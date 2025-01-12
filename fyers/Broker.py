from .authentication.Authenticator import Authenticator

class Broker:
    
    __INSTANCE = None
    
    def __init__(self):
        self.__fyers_instance = None
               
    @staticmethod
    def getInstance():        
        if Broker.__INSTANCE is None:
            broker = Broker()
            broker.authenticate()
            Broker.__INSTANCE = broker
        return Broker.__INSTANCE
        
    def authenticate(self):
        self.__fyers_instance = Authenticator.getAuthenticatedFyersIntance()
        
    def get_funds(self):
        return self.__fyers_instance.funds()
    
    def get_holdings(self):
        return self.__fyers_instance.holdings()
    
    def get_historical_data(self,data):
        return self.__fyers_instance.history(data=data)