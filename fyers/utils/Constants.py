from pathlib import Path
from dotenv import load_dotenv
import os

class Constants():

    load_dotenv()
    TOTP_SECRET = os.getenv("TOTP_SECRET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    PIN = os.getenv("PIN")
    
    APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
    APP_REDIRECT_URI = os.getenv("APP_REDIRECT_URI")
    APP_RESPONSE_CODE = os.getenv("APP_RESPONSE_CODE")
    APP_GRANT_TYPE = os.getenv("APP_GRANT_TYPE")
    
    DIR_ROOT = Path(__file__).resolve().parent.parent
    
    DIR_FYERS_AUTH_TOKENS = DIR_ROOT.joinpath("tokens/fyers_auth_token")
    FILENAME_FYERS_AUTH_TOKENS = "fyers_auth_config.json"
    PATH_FYERS_AUTH_TOKENS = DIR_FYERS_AUTH_TOKENS.joinpath(FILENAME_FYERS_AUTH_TOKENS)
    
    DIR_APP_AUTH_TOKENS = DIR_ROOT.joinpath("tokens/app_auth_token")
    FILENAME_APP_AUTH_TOKENS = "app_auth_config.json"
    PATH_APP_AUTH_TOKENS = DIR_APP_AUTH_TOKENS.joinpath(FILENAME_APP_AUTH_TOKENS)
    
    DIR_HISTORICAL_DATA = DIR_ROOT.joinpath("outputs/historical_data")
    
       
    URL_APP_REFRESH_TOKEN = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
    URL_SEND_LOGIN_OTP = "https://api-t2.fyers.in/vagator/v2/send_login_otp_v2"
    URL_VERIFY_OTP = "https://api-t2.fyers.in/vagator/v2/verify_otp"
    URL_VERIFY_PIN = "https://api-t2.fyers.in/vagator/v2/verify_pin_v2"
    URL_VALIDATE_TOKENS = "https://api-t1.fyers.in/gk/validate_tokens"
    URL_GET_AUTH_CODE = "https://api.fyers.in/api/v2/token"
       
    
    DIR_LOGS = DIR_ROOT.joinpath("logs")
    
    