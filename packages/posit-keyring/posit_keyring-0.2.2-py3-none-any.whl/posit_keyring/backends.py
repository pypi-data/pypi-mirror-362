import os
import platform
import time
import webbrowser
from typing import Any
from urllib.parse import urlparse

import keyring
import keyring.backend
import requests
from jaraco.classes.properties import classproperty
from keyring.backends.kwallet import DBusKeyring as KWalletKeyring
from keyring.backends.libsecret import Keyring as LibSecretKeyring
from keyring.backends.macOS import Keyring as MacOSKeyring
from keyring.backends.SecretService import Keyring as SecretServiceKeyring
from keyring.backends.Windows import WinVaultKeyring
from keyring.errors import KeyringError

from . import pkce


# This is a custom keyring backend for the Posit Package Manager.
# It handles the OAuth 2.0 device flow for user authentication and token management.
# It is designed to work with the Posit Package Manager's API for token exchange and authentication.
# The backend will automatically handle the device authorization flow if no token is found in the system keyring.
# It will also store the token securely in the system keyring after successful authentication.
# If the token is expired, it will automatically go through the device flow again to refresh the token.
# The backend can also bypass the device flow by setting the PACKAGEMANAGER_IDENTITY_TOKEN_FILE environment variable
# to a file containing the identity token.
# This allows the backend to directly exchange the identity token for a Package Manager token without user interaction.
# The backend supports multiple platforms (macOS, Windows, Linux) using the appropriate keyring system keyring backend.
# It is designed to be used with the `keyring` library, which provides a
# unified interface for accessing system keyrings.
class PackageManagerKeyring(keyring.backend.KeyringBackend):

    # Set a higher priority for this custom keyring backend.
    # This makes it more likely to be chosen by the keyring library
    # if multiple backends are available.
    @classproperty
    def priority(self) -> float:
        return 10

    def __init__(self):
        """
        Initializes the keyring backend.
        It retrieves the Posit Package Manager URL from the
        PACKAGEMANAGER_ADDRESS environment variable. This URL is crucial
        for all API interactions and for determining the service name
        this backend will manage.
        """
        # Initialize the base KeyringBackend class
        super().__init__()

        self.ppm_url = os.getenv("PACKAGEMANAGER_ADDRESS")
        if not self.ppm_url:
            # Don't raise an error, just make this backend non-viable
            self._config()
            return

        # Parse the PPM URL to extract the netloc (hostname:port). This will be used
        # as the 'service' name that this keyring backend responds to, ensuring it
        # matches what pip passes for URLs with explicit ports.
        parsed_url = urlparse(self.ppm_url)
        if not parsed_url.netloc:  # Use netloc instead of hostname
            # Don't raise an error, just make this backend non-viable
            self._config()
            return

        system_keyring = self._select_keyring()
        if not system_keyring:
            # Don't raise an error, just make this backend non-viable
            self._config()
            return

        # Set the keyring backend with the valid configuration
        self._config(
            ppm_url=self.ppm_url,
            service_name=parsed_url.netloc,
            system_keyring=system_keyring,
            viable=True,
        )

    def get_password(self, service: str, username: str) -> str | None:
        # Return None if:
        # - the backend is not properly configured
        # - the service does not match the PPM URL or the service name
        # - the username is not "__token__"
        # - the PPM URL is not set
        if (
            not self._viable
            or not self._requirements_valid(service, username)
            or not self.ppm_url
        ):
            return None

        # Check if the PPM token is already stored and that the token is valid
        existing_token = (
            self.keyring.get_password(self.ppm_url, "__token__")
            if self.keyring
            else None
        )
        if existing_token and self._can_authenticate(
            self.ppm_url, ("__token__", existing_token)
        ):
            return existing_token

        # If the token is not available or invalid, initiate the authentication
        # process
        try:
            # Get the identity token from the environment variable if it exists
            identity_token = self._get_identity_token()

            # If no identity token is provided, initiate the device
            # authorization flow
            if not identity_token:
                identity_token = self._device_flow()

            # Exchange the identity token for a PPM access token
            ppm_token = self._identity_to_ppm_token(identity_token)
            self.keyring.set_password(  # type:ignore
                self.ppm_url, "__token__", ppm_token
            )

            return ppm_token

        except Exception as e:
            print(f"Authentication process failed: {e}")
            return None

    def set_password(self, service: str, username: str, password: str) -> None:
        # Defer setting a password to the next backend
        raise NotImplementedError()

    def delete_password(self, service: str, username: str) -> None:
        # Defer deleting a password to the next backend
        raise NotImplementedError()

    def _init_device_auth(self, challenge: str) -> dict[str, Any]:
        """
        Initiates the OIDC device authorization flow, requiring a PKCE code challenge.

        Returns:
            dict: The JSON response containing `device_code`, `user_code`,
                  `verification_uri`, `verification_uri_complete`, etc.
        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
        """
        url = f"{self.ppm_url}/__api__/device?code_challenge_method=S256&code_challenge={challenge}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()

    def _complete_device_auth(
        self,
        device_auth_response: dict[str, Any],
        interval: int,
        expires_in: int,
    ) -> dict[str, Any] | None:
        """
        Polls the OIDC provider to complete the device authorization flow.

        Args:
            device_auth_response (dict): The initial response from `_init_device_auth`.
            interval (int): The polling interval in seconds.
            expires_in (int): The timeout for the authorization in seconds.

        Returns:
            dict | None: The JSON response containing the `id_token` if successful, otherwise None.
        Raises:
            Exception: If access is denied, token expires, or unexpected errors occur.
        """
        url = f"{self.ppm_url}/__api__/device_access"
        device_code = device_auth_response.get("device_code")
        if not device_code:
            raise ValueError(
                "Device code not found in initial device authorization response."
            )

        start_time = time.time()
        while time.time() - start_time < expires_in:
            # Send the entire device_auth_response, not just the device_code
            response = requests.post(url, json=device_auth_response)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                error_code = error_data.get("error")
                error_description = error_data.get(
                    "error_description", "No description provided."
                )

                if error_code == "authorization_pending" or error_code == "slow_down":
                    # User hasn't authorized yet, or polling too fast. Wait and
                    # retry.
                    pass  # We'll sleep below
                elif error_code == "access_denied":
                    raise Exception(f"Access denied by user: {error_description}")
                elif error_code == "expired_token":
                    raise Exception(
                        f"Device authorization request expired: {error_description}"
                    )
                else:
                    raise Exception(
                        f"Unexpected error during device authorization ({error_code}): {error_description}"
                    )
            else:
                response.raise_for_status()  # Raise for other unexpected HTTP errors

            time.sleep(interval)  # Wait before polling again

        raise Exception("Device authorization timed out. Please try again.")

    def _token_exchange(self, sso_token: str) -> dict[str, Any]:
        """
        Exchanges the OIDC ID token for a PPM access token.

        Args:
            sso_token (str): The ID token obtained from the OIDC provider.

        Returns:
            dict: The JSON response containing the `access_token` (PPM token).
        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
        """
        url = f"{self.ppm_url}/__api__/token"
        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": sso_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()

    def _open_url(self, url: str) -> None:
        """
        Opens a URL in the default web browser.

        Args:
            url (str): The URL to open.
        """
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please manually open this URL: {url}")

    def _can_authenticate(self, url: str, auth: tuple[str, str]) -> bool:
        response = requests.get(url, auth=auth)

        return (
            response.status_code < 500
            and response.status_code != 401
            and response.status_code != 403
        )

    def _requirements_valid(self, service: str, username: str) -> bool:
        """
        Verifies if the service matches the PPM URL or the service name
        and that the username is "__token__".

        Args:
            service (str): The service to verify.

        Returns:
            bool: True if the service matches, False otherwise.
        """

        # Normalize the service to handle full URLs and netloc
        parsed_service = urlparse(service)
        service_netloc = parsed_service.netloc
        service_scheme = parsed_service.scheme

        # Handle the case where service is just "host:port" without scheme
        # In this case, urlparse treats "host" as scheme and "port" as path
        if (
            not service_netloc
            and ":" in service
            and not service.startswith(("http://", "https://"))
        ):
            # This is likely a "host:port" format, treat the whole thing as
            # netloc
            service_netloc = service

        # Handle the service if it matches the netloc OR if it starts with the
        # PPM URL
        service_matches = service_netloc == self.service_name or (
            service_scheme and self.ppm_url and service.startswith(self.ppm_url)
        )
        username_check = username != "__token__"

        if not service_matches or username_check:
            return False

        return True

    def _get_identity_token(self) -> str | None:
        """
        Retrieves the identity token from the PACKAGEMANAGER_IDENTITY_TOKEN_FILE environment variable.

        Returns:
            str | None: The identity token if available, otherwise None.
        """
        identity_token_file = os.getenv("PACKAGEMANAGER_IDENTITY_TOKEN_FILE")
        if identity_token_file:
            try:
                with open(identity_token_file, "r") as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Failed to read identity token file: {e}")
                return None
        return None

    def _config(
        self,
        ppm_url: str | None = None,
        service_name: str | None = None,
        system_keyring: keyring.backend.KeyringBackend | None = None,
        viable: bool = False,
    ) -> None:
        self.ppm_url = ppm_url
        self.service_name = service_name
        self.keyring = system_keyring
        self._viable = viable

    def _select_keyring(self) -> keyring.backend.KeyringBackend | None:
        """Identifies the system and selects the appropriate default keyring."""
        system = platform.system().lower()

        if system == "darwin":  # macOS
            return MacOSKeyring()
        elif system == "windows":  # Windows
            return WinVaultKeyring()
        elif system == "linux":  # Linux
            # Prefer SecretService (GNOME Keyring) if available
            try:
                secret_service = SecretServiceKeyring()
                if secret_service.priority > 0:
                    return secret_service
            except KeyringError:
                pass
            # Fallback to libsecret (GNOME Keyring) if SecretService is not
            # available
            try:
                libsecret = LibSecretKeyring()
                if libsecret.priority > 0:
                    return libsecret
            except KeyringError:
                pass
            # Fallback to KWallet (KDE Wallet) if SecretService and libsecret
            # is not available
            try:
                kwallet = KWalletKeyring()
                if kwallet.priority > 0:
                    return kwallet
            except KeyringError:
                pass
            # Raise error if no suitable keyring is found
            raise KeyringError("No suitable keyring backend found for Linux")
        else:
            raise KeyringError(f"Unsupported platform: {system}")

    def _device_flow(self) -> str:
        """
        Initiates the device authorization flow and returns the identity token.

        Returns:
            str: The identity token obtained from the device authorization flow.
            None: If the device authorization flow fails or is denied.
        Raises:
            Exception: If the device authorization flow fails or is denied.
        """

        try:
            code_verifier = pkce.new_pkce_verifier()

        except ValueError:
            raise ValueError("{e}")

        code_challenge = pkce.new_pkce_challenge(code_verifier)

        device_auth_response = self._init_device_auth(code_challenge)
        user_code = device_auth_response.get("user_code")
        verification_uri = device_auth_response.get("verification_uri")
        verification_uri_complete = device_auth_response.get(
            "verification_uri_complete"
        )
        interval = device_auth_response.get("interval", 5)
        expires_in = device_auth_response.get("expires_in", 300)

        display_uri = (
            verification_uri_complete if verification_uri_complete else verification_uri
        )
        if not display_uri:
            raise ValueError(
                "No verification URI available from device authorization response"
            )

        print("\nPlease open the following URL in your browser:")
        print(f"  {display_uri}")
        print("\nAnd enter the following code when prompted:")
        print(f"  {user_code}")
        print("\nWaiting for authorization...")

        self._open_url(display_uri)

        # Add the code_verifier to the device_auth_response for PKCE
        device_auth_response["code_verifier"] = code_verifier

        identity_token_response = self._complete_device_auth(
            device_auth_response, interval, expires_in
        )
        if not identity_token_response or "id_token" not in identity_token_response:
            raise Exception(
                "Failed to complete device authorization or obtain identity token."
            )

        return identity_token_response["id_token"]

    def _identity_to_ppm_token(self, identity_token: str) -> str:
        """
        Exchanges the identity token for a PPM access token.

        Args:
            identity_token (str): The identity token obtained from the OIDC provider.
            service (str): The service name to use for the token exchange.

        Returns:
            str: The PPM access token.
        Raises:
            Exception: If the token exchange fails or is denied.
        """
        token_exchange_response = self._token_exchange(identity_token)
        if not token_exchange_response or "access_token" not in token_exchange_response:
            raise Exception("Failed to exchange identity token for PPM access token.")

        return token_exchange_response["access_token"]
