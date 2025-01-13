from .authentication.Authenticator import Authenticator

class Broker:
    
    __INSTANCE = None
    
    def __new__(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
            
        return cls.__INSTANCE
    
    def __init__(self):
        self.__fyers_instance = None
        self.authenticate()
        
    def authenticate(self):
        self.__fyers_instance = Authenticator.getAuthenticatedFyersIntance()
        return
        
    def get_funds(self):
        return self.__fyers_instance.funds()
    
    def get_holdings(self):
        return self.__fyers_instance.holdings()
    
    def get_historical_data(self,data):
        return self.__fyers_instance.history(data=data)