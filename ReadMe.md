# Fyers Trading Module

This project is a full-fledged trading cum data gathering application built on top of Fyers Python SDK. Fyers Trading Module is built with the focus of Algo Trading and Backtesting use-cases.

## Use cases of this project

- Algo Trading
- Accessing Live Market Feed
- Donwloading Historical Data
- Data Analysis
- Backtesting
- Account Analysis

## Prerequisites

Before setting up the project, make sure the following are installed in your machine:

- **Python (>= 3.x)**
- **pip** (Python package manager)
- **Enabled 2FA using TOTP in Fyers Account** ([Tutorial](https://support.fyers.in/portal/en/kb/articles/how-to-set-up-time-based-one-time-password-totp-in-fyers))
- **Created and Activated Fyers API APP**([Tutorial](https://myapi.fyers.in))

# Setup Instructions (Windows Machine)

Follow these steps to set up the project and run it on your machine.

## 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/iamrishiksahu/fyers-trading-module.git

cd fyers-trading-module
```

## 2. Setting Up Virtual Environment
To create the virtual environment, run the following command:
```bash
python -m venv fyers
```
To acivate the environment, run:
```bash
fyers\Scripts\activate.bat
```


## 3. Installing Dependencies
```bash
pip install -r requirements.txt
```

## 4. Creating the `.env` File

To securely store sensitive environment variables, create a .env file in the root of your project directory.

Add the following variables to your `.env` file:

```bash
TOTP_SECRET=<your-totp-secret>
CLIENT_ID=<your-user-id-used-to-login>
PIN=<your-login-pin>

APP_CLIENT_ID=<your-app-client-id>
APP_SECRET_KEY=<your-app-secret-key>
APP_REDIRECT_URI=<your-app-redirect-uri>
APP_RESPONSE_CODE=<your-app-response-code>
APP_GRANT_TYPE=<your-app-grant-type>
```
## 4. Running The Application
```bash
python -m fyers
```

# Documentation

Here's a detailed documentation on how you can use the application for specific use-cases.

[Read Docs](./Documentation.md)

# Contribution

This project is open to get contributions by individuals. You are welcoome to contribute and help this project grow.

# Disclaimer

This project is solely meant for educational and tutorial purposes only. The owner, contributor(s) or maintainer(s) of the project do not advise scripts for trading and none of them holds any responisbility for any failures, unexpected execution or performance related issues that might encounter during the use of this module. The entire project is open-source and hence it is advised to check the source code and modify upto your satisfaction before placing orders. 

Trading in capital markets is subjected to financial risks. It is advised to perform proper risk analysis before executing orders.

# Contact
[LinkedIn](https://linkedin.com/in/rishiksahubit)