# Posit Device Flow Keyring Backend

This is a custom Python keyring backend for the Posit Package Manager. It allows the handling of OAuth2 device flow and token exchange to securely store and retrieve Package Manager tokens.

- Implements OAuth 2.0 device flow for user authentication if no token exists in the system keyring.
- Stores the token securely in the system keyring after successful authentication.
- If the Package Manager token is expired, it will automatically go through the device flow again to refresh the token.
- Ability to bypass the device flow by setting the `PACKAGEMANAGER_IDENTITY_TOKEN_FILE` environment variable to a file containing the identity token. This will allow the backend to directly exchange the identity token for a Package Manager token without user interaction.
- Supports multiple platforms (macOS, Windows, Linux) using the appropriate keyring system keyring backend.

## Quick Start

This is a quick guide to get started with the Posit Package Manager keyring backend. This assumes Package Manager is already configured to use authenticated repositories. The steps assume a Unix-like environment (Linux/macOS). For Windows, the commands may vary slightly, and are provided in the more detailed instructions below.

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install the posit-keyring package
pip install posit-keyring

# You may have to refresh your shell cache to ensure the keyring backend is recognized
hash -r

# Set the environment variable for the Package Manager address
export PACKAGEMANAGER_ADDRESS="https://your-ppm-instance.com"

# Set the environment variable for the pip index URL
export PIP_INDEX_URL="https://__token__@your-ppm-instance.com/pypi-auth/latest/simple/"

# Set the environment variables for twine
export TWINE_REPOSITORY_URL="https://your-ppm-instance.com/upload/pypi/local-python-src"
export TWINE_USERNAME="__token__"

# Use pip to install packages
pip install your-package

# Use twine to upload packages
twine upload dist/*
```

Below will provide more detailed instructions on the various configuration options when using this keyring backend.

## Installation

To use this keyring backend, you need to install `posit-keyring`:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the package, this will install the keyring as a dependency if not already installed
pip install posit-keyring

# You may have to refresh your shell cache to ensure the keyring backend is recognized
hash -r
```

It is good to verify that the `keyring` package is installed correctly and that the backend is set up properly.

```bash
# Verify you are using the Python keyring package in the virtual environment
which keyring # On Windows use `where keyring`

# Verify the keyring backend is set up correctly
keyring --list-backends
# You should see posit_keyring.backends.PackageManagerKeyring
```

Now you can use this keyring backend for installing and uploading packages with the Posit Package Manager.

## Setup

### Environment Variables

#### Package Manager
To set up the Posit Package Manager keyring backend, you need to ensure that the `PACKAGEMANAGER_ADDRESS` environment variable is set to the URL of your PPM instance. This can be done in your shell configuration file (e.g., `.bashrc`, `.zshrc`, or `.bash_profile`).

```bash
export PACKAGEMANAGER_ADDRESS="https://your-ppm-instance.com"

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc, etc.
```

Or on Windows, set the environment variable in PowerShell or Command Prompt.
```powershell
$env:PACKAGEMANAGER_ADDRESS = "https://your-ppm-instance.com"
```

#### Identity Token
A common pattern is to store the identity token in a file, which can be referenced by the `PACKAGEMANAGER_IDENTITY_TOKEN_FILE` environment variable. This file should contain the token string.

```bash
# Create a file to store the identity token
echo "your-identity-token" > ~/identity_token.txt
export PACKAGEMANAGER_IDENTITY_TOKEN_FILE=~/identity_token.txt

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc, etc.
```

Or on Windows, set the environment variable in PowerShell or Command Prompt.
```powershell
New-Item -Path $env:USERPROFILE -Name "identity_token.txt" -ItemType "file" -Value "your-identity-token"
$env:PACKAGEMANAGER_IDENTITY_TOKEN_FILE = "$env:USERPROFILE\identity_token.txt"
```

Setting this will allow the keyring backend to read the identity token from the specified file. If you do not set this variable, the backend will prompt you to authenticate using the OAuth2 device flow. Setting it skips the flow entirely and directly exchanges the identity token for a Package Manager token.

### Posit Package Manager Server Configuration
In Package Manager, you will want to create an authenticated Python repository. This can be done by running the following command:

```bash
# create an authenticated Python repository in Posit Package Manager
rspm create repo --name=pypi-auth --type=python --authenticated

# subscribe the PyPI mirror to the new authenticated repository
rspm subscribe --repo=pypi-auth --source=pypi

# if you have local packages you want to upload, you can also create a local repository
rspm create source --name=local-python-src --type=local-python
rspm subscribe --repo=pypi-auth --source=local-python
```

The server should be configured with the `OpenIDConnect` and/or `IdentityFederation` configuration options to enable device flow authentication. This is documented in the Admin Guide for Posit Package Manager.

### Pip Configuration
Then you can set your `pip` configuration to use the new authenticated repository by creating or editing the `pip.conf` file (or `pip.ini` on Windows) in your home directory:

```ini
# ~/.config/pip/pip.conf (Linux/macOS)
[global]
index-url = https://__token__@your-ppm-instance.com/pypi-auth/latest/simple/

# %APPDATA%\pip\pip.ini (Windows)
[global]
index-url = https://__token__@your-ppm-instance.com/pypi-auth/latest/simple/
```

Alternatively, you can set the `PIP_INDEX_URL` environment variable to point to your PPM instance:

```bash
export PIP_INDEX_URL="https://__token__@your-ppm-instance.com/pypi-auth/latest/simple/"

# Reload your shell configuration if saved in .bashrc or .zshrc
source ~/.bashrc  # or source ~/.zshrc, etc.
```

Or on Windows, set the environment variable in PowerShell or Command Prompt.
```powershell
$env:PIP_INDEX_URL = "https://__token__@your-ppm-instance.com/pypi-auth/latest/simple/"
```

> [!NOTE]
> If everything is configured properly, `keyring` should give this backend the highest priority automatically. Sometimes a `keyringrc.cfg` file exists that causes issues. You can delete it to force the keyring to use the correct backend:
>
> ```bash
> rm ~/.config/python_keyring/keyringrc.cfg  # Linux/macOS
> del %APPDATA%\python_keyring\keyringrc.cfg  # Windows
> ```
>
> You can also manually specify the backend in your `pip.conf` or `pip.ini` file with:
>
> ```ini
> [global]
> keyring_backend = posit_keyring.backends.PackageManagerKeyring
> ```
>
> Or with an environment variable (mentioned in [these docs](https://pypi.org/project/keyring/)):
>
> ```bash
> export PYTHON_KEYRING_BACKEND="posit_keyring.backends.PackageManagerKeyring" # Linux/macOS
> $env:PYTHON_KEYRING_BACKEND="posit_keyring.backends.PackageManagerKeyring" # Windows
> ```
>
> If the virtual environment is not detecting the keyring backend, you may have to refresh your shell cache to ensure it is recognized:
>
> ```bash
> hash -r
> ```

### Twine Configuration
If you are using `twine` to upload packages, you can also configure it to use the Posit Package Manager keyring backend by creating or editing the `pypirc` file in your home directory:
```ini
# ~/.pypirc (Linux/macOS)
[distutils]
index-servers =
    package-manager

[package-manager]
repository = https://your-ppm-instance.com/upload/pypi/local-python-src
username = __token__

# %APPDATA%\.pypirc (Windows)
[distutils]
index-servers =
    package-manager

[package-manager]
repository = https://your-ppm-instance.com/upload/pypi/local-python-src
username = __token__
```

Alternatively, you can set the `TWINE_REPOSITORY_URL` environment variable to point to your PPM instance:

```bash
export TWINE_REPOSITORY_URL="https://your-ppm-instance.com/upload/pypi/local-python-src"
export TWINE_USERNAME="__token__"

# Reload your shell configuration if saved in .bashrc or .zshrc
source ~/.bashrc  # or source ~/.zshrc, etc.
```

Or on Windows, set the environment variables in PowerShell or Command Prompt.
```powershell
$env:TWINE_REPOSITORY_URL = "https://your-ppm-instance.com/upload/pypi/local-python-src"
$env:TWINE_USERNAME = "__token__"
```

## Usage

Once the backend is set up, you can use `pip` and `twine` commands to install and upload packages, and the keyring backend will handle authentication the authentication flow automatically.

```bash
# Install a package
pip install your-package

# Upload a package
twine upload dist/* # include `-r package-manager` if you configured twine with `.pypirc`
```

## Development

### Prerequisites
- Python 3.8 or later installed
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)

### Cloning the Repository
To get `posit-keyring` locally, you can clone the repository:

```bash
git clone https://github.com/posit-dev/posit-keyring.git
cd posit-keyring
```

### Setting up the Development Environment
There is a `just` task to set up the development environment, which will create a virtual environment and install the required dependencies:
```bash
# Create the virtual environment with the required dependencies from the uv.lock file
just sync

# Activate the created virtual environment
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

To run the package locally in editable mode:
```bash
just install
```

You can also run linting and type checking with:
```bash
# Run linting
just lint

# Run type checking
just type
```