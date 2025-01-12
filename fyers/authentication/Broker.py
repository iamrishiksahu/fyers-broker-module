import requests
import json
import pyotp
from datetime import datetime
import time
import base64
import os
from fyers_apiv3 import fyersModel
from urllib.parse import urlparse, parse_qs
from ..utils.MainUtil import MainUtil  
from ..utils.Constants import Constants 
from ..utils.Logger import Logger
from ..utils.ApiUtil import APIUtil

class Broker:
    TOTP_SECRET = Constants.TOTP_SECRET
    CLIENT_ID = Constants.CLIENT_ID
    PIN = Constants.PIN
    
    APP_CLIENT_ID = Constants.APP_CLIENT_ID
    APP_SECRET_KEY = Constants.APP_SECRET_KEY
    APP_REDIRECT_URI = Constants.APP_REDIRECT_URI
    APP_RESPONSE_CODE = Constants.APP_RESPONSE_CODE
    APP_GRANT_TYPE = Constants.APP_GRANT_TYPE
    
    __INSTANCE = None
    
    MAX_FETCH_APP_KEYS_RETRY_COUNT = 3
    MAX_MAIN_RETRY_COUNT = 3
    MAX_INITIALIZE_RETRY_COUNT = 3
    
    @staticmethod
    def getInstance():
        if Broker.__INSTANCE is None:
            broker = Broker()
            broker.main()
            return broker
        return Broker.__INSTANCE

    def instantiate(self):
        return self.getInstance()

    # Set headers
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    }

    def send_login_otp(self, session, client_id):
        """Send login OTP"""
        payload = {
            "fy_id": base64.b64encode(f"{client_id}".encode()).decode(),
            "app_id": "2"
        }
        
        try:
            response = APIUtil.post(Constants.URL_SEND_LOGIN_OTP, session=session, json_data=payload)
            response.raise_for_status()
            return response.json()["request_key"]
        except requests.exceptions.RequestException as e:
            Logger.log(f"Error while sending OTP: {e}")
            return None

    def verify_otp(self, session, request_key, otp):
        """Verify OTP"""
        if datetime.now().second >= 57 or datetime.now().second <= 3:
            time.sleep(6)

        try:
            response = APIUtil.post(Constants.URL_VERIFY_OTP, session=session, json_data={"request_key": request_key, "otp": otp})
            response.raise_for_status()
            return response.json()["request_key"]
        except requests.exceptions.RequestException as e:
            Logger.log(f"Error occurred while verify OTP: {e}")
            return None

    def verify_pin(self, session, request_key, pin):
        """Verify PIN"""
        try:
            response = APIUtil.post(Constants.URL_VERIFY_PIN, session=session, json_data={"request_key": request_key, "identifier": base64.b64encode(f"{pin}".encode()).decode(), "identity_type": "pin"})
            response.raise_for_status()
            return {"refresh_token": response.json()["data"]["refresh_token"], "access_token": response.json()["data"]["access_token"]}
        except requests.exceptions.RequestException as e:
            Logger.log(f"Error occurred while verify PIN: {e}")
            return None

    def validateAuthTokens(self, access_token, refresh_token):
        """Validate tokens"""
        try:    
            response = APIUtil.get(Constants.URL_VALIDATE_TOKENS, headers={
                "Authorization": f"{access_token}",
                "Refresh_token": f"{refresh_token}"
               })
            if response.status_code != 200:
                Logger.log("Error occurred while validating tokens: ", response.json())
                return False
            
            res = response.json()
            
            if "validate_access_token" in res and "validate_refresh_token" in res:
                if res["validate_access_token"] and res["validate_refresh_token"]:
                    return 1 # All Valid
                elif res["validate_refresh_token"]:                
                    return 2 # Only Refresh
                else:
                    return 3 # None valid
        except requests.exceptions.RequestException as e:
            Logger.log(f"Exception occurred while validating tokens : {e}")
            return False
        
    def getTokensByLogin(self):
        # Create a session
        current_network_session = requests.Session()
        current_network_session.headers.update(Broker.headers)
        
        request_key_for_otp = self.send_login_otp(current_network_session, Broker.CLIENT_ID)
        request_key_for_pin = self.verify_otp(current_network_session, request_key_for_otp, pyotp.TOTP(Broker.TOTP_SECRET).now())
        final_response = self.verify_pin(current_network_session, request_key_for_pin, Broker.PIN)

        if final_response is not None and "access_token" in final_response and "refresh_token" in final_response:
            json_res = {
                "refresh_token": final_response["refresh_token"],
                "access_token": final_response["access_token"]
            }
            MainUtil.writeFile(Constants.PATH_FYERS_AUTH_TOKENS, json.dumps(json_res))
            return [final_response["access_token"], final_response["refresh_token"]]
        else:
            Logger.log("Could not get fyers auth tokens by login, some error occured.")
            return None
        
    def getAuthTokens(self):
        """Get Saved Tokens From File"""
        access_token = ""
        refresh_token = ""
        try:
            file_contents = MainUtil.readFile(Constants.PATH_FYERS_AUTH_TOKENS)
            json_res = json.loads(file_contents) 
            
            if json_res["access_token"] is not None and json_res["refresh_token"] is not None:
                Logger.log("Returning existing auth tokens")
                return [json_res["access_token"], json_res["refresh_token"]]
            return None
            
            
        except Exception as e:
            Logger.log(e)
            Logger.log("No fyers auth tokens saved, Trying to get tokens by login!")
            try:
                res = self.getTokensByLogin()
                if res is not None:
                    access_token = res[0]
                    refresh_token = res[1]
                    return [access_token, refresh_token]
                else:
                    raise Exception("getTokensByLogin resulted in a null response.")
            except Exception as eIn:
                Logger.log(eIn)
        
        return None
                
    def getAccessTokenFromRefreshToken(self, ):
        refresh_token = ""
        try:
            with open("fyers_auth_tokens/refresh_token.txt", "r") as file:
                refresh_token = file.readline()
        except Exception as e:
            Logger.log(e)
            
    def getAuthCode(self, access_token):
        headers = {
            "Authorization" : f"Bearer {access_token}",
            "Content-Type" : "application/json",
            "Charset" : "UTF-8"
        }
        
        payload = {
            "fyers_id" : Broker.CLIENT_ID,
            "app_id" : Broker.APP_CLIENT_ID.split("-")[0],
            "redirect_uri": Broker.APP_REDIRECT_URI,
            "appType" :Broker.APP_CLIENT_ID.split("-")[1],
            "code_challenge": "",
            "state": "abcdefg",
            "scope": "",
            "nonce": "",
            "response_type": "code",
            "create_cookie": True
        }   
        
        try:
            res = requests.post(Constants.URL_GET_AUTH_CODE, headers=headers, json=payload)
            parsedRedirectUrl = urlparse(res.json()["Url"])
            auth_code = parse_qs(parsedRedirectUrl.query)["auth_code"][0]
            
            file_contents = MainUtil.readFile(Constants.PATH_APP_AUTH_TOKENS)
            if file_contents is None:
                file_contents = "{}"
            
            json_data = json.loads(file_contents)
            json_data["auth_code"] = auth_code
            MainUtil.writeFile(Constants.PATH_APP_AUTH_TOKENS, json.dumps(json_data))
            return auth_code
        except Exception as e:
            Logger.log(e)
            return None       
    
    def generateAppAccessTokenFromRefreshToken(self):
        
        try:           
        
            file_contents = MainUtil.readFile(Constants.PATH_APP_AUTH_TOKENS)
            json_data = json.loads(file_contents)
            
            app_refresh_token = json_data['refresh_token']
            if app_refresh_token is None:
                return None
            
            res = requests.post(Constants.URL_APP_REFRESH_TOKEN, json={
                "grant_type": "refresh_token",
                "appIdHash": MainUtil.getSHA256Hash(Broker.APP_CLIENT_ID + ":" + Broker.APP_SECRET_KEY),
                "refresh_token": app_refresh_token,
                "pin": Broker.PIN            
            })

            if res.status_code == 200:
                new_access_token = res.json()['access_token']
                json_data["access_token"] = new_access_token
                json_data["created_date"] = str(datetime.today().date())
                json_data["time"] = str(datetime.now())
                MainUtil.writeFile(Constants.PATH_APP_AUTH_TOKENS, json.dumps(json_data))
                Logger.log("Refreshed the App Access Token from App Refresh Token")
                return new_access_token
            Logger.log("App refresh token expired! Generate another.")      
            return None
        except Exception as e:
            Logger.log(e)  
            return None
       
    def initializeFyersModule(self, access_token, retryCount = 0):
        
        if retryCount > Broker.MAX_INITIALIZE_RETRY_COUNT:
            Logger.log("Retry count exceeded for initializeFyersModule")
            return
        
        self.__appInstance = fyersModel.FyersModel(client_id=Broker.CLIENT_ID, token=access_token,is_async=False, log_path="")
        funds_res = self.__appInstance.funds()
        
        if funds_res['code'] == 200:
            Logger.log("Broker initialized successfully!")
        else:
            # Problem with initialization, app access_token is invalid, regenerate it
            Logger.log("Error initializing the fyers module. Retry gaining tokens")
            new_access_token = self.generateAppAccessTokenFromRefreshToken()
            if new_access_token is not None:
                self.initializeFyersModule(new_access_token, retryCount=retryCount+1)
                return
            else:
                MainUtil.deleteFile(Constants.PATH_APP_AUTH_TOKENS)
                self.main()
                pass
        
    def fetchAppKeys(self, retryCount = 0):
        
        if retryCount > Broker.MAX_FETCH_APP_KEYS_RETRY_COUNT:
            Logger.log("Max retry limit reached for fetchAppKeys Method. ")
            return
        
        [access_token, refresh_token] = self.getAuthTokens()
        # Validating the auth tokens is an optional step, not required
        tokenValidityStatus = self.validateAuthTokens(access_token,refresh_token)
        Logger.log("Auth Tokens Validity Status: ",tokenValidityStatus)

        if tokenValidityStatus == 1 :        
            auth_code = self.getAuthCode(access_token)                   
            app_session = fyersModel.SessionModel(
                client_id=Broker.APP_CLIENT_ID,
                secret_key=Broker.APP_SECRET_KEY, 
                redirect_uri=Broker.APP_REDIRECT_URI, 
                response_type=Broker.APP_RESPONSE_CODE, 
                grant_type=Broker.APP_GRANT_TYPE
            )
            app_session.set_token(auth_code)
            app_auth_response = app_session.generate_token()
            
            if app_auth_response["code"] == 200:      
                
                
                file_contents = MainUtil.readFile(Constants.PATH_APP_AUTH_TOKENS)
                if file_contents is None:
                    file_contents = "{}"
                    
                json_data = json.loads(file_contents)
                
                json_data["access_token"] =  app_auth_response["access_token"]
                json_data["refresh_token"] =  app_auth_response["refresh_token"]
                json_data["time"]  =  str(datetime.now())
                json_data["created_date"]  =  str(datetime.today().date())
                
                
                MainUtil.writeFile(Constants.PATH_APP_AUTH_TOKENS,json.dumps(json_data))
                return json_data["access_token"]
            else:
                Logger.log("Could not get access and refresh token while creating the App Session.")
                return None
        elif tokenValidityStatus == 2:
            # TODO: Generate fyers access token using fyers refresh token
            # Currently generating both for simplicity
            MainUtil.deleteFile(Constants.PATH_FYERS_AUTH_TOKENS)
            self.fetchAppKeys(retryCount=retryCount+1)        
            pass
        elif tokenValidityStatus == 3:
            # Generate both tokens from start  
            MainUtil.deleteFile(Constants.PATH_FYERS_AUTH_TOKENS)
            self.fetchAppKeys(retryCount=retryCount+1)  
            
    def getAppKeys(self):
        try:                
            file_contents = MainUtil.readFile(Constants.PATH_APP_AUTH_TOKENS)
            config_data = json.loads(file_contents)
            # If the date is same date, we can use the token, else generate new
            if config_data['created_date'] == str(datetime.today().date()):
                Logger.log("App Access Token Available! Using the same.")
                return config_data["access_token"]
            else:
                # This case is handled automatically in the initializeFyersModule function
                return ""

        except Exception as e:
            Logger.log(e)   
        
        Logger.log("Generating new App Access Token")   
        app_access_token = self.fetchAppKeys()
        if app_access_token is not None:
            return app_access_token
        
    def main(self):

        app_access_token = self.getAppKeys()
        self.initializeFyersModule(app_access_token)

            
    def get_funds(self):
        return self.__appInstance.funds()
    
    def get_holdings(self):
        return self.__appInstance.holdings()
    
    def history(self,data):
        return self.__appInstance.history(data=data)
    

