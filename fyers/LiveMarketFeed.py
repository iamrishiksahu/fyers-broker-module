from utils.MainUtil import MainUtil
from utils.Logger import Logger, LogType
from utils.Constants import Constants
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime
import socketio
import json
from utils.SocketUtility import SocketUtility

sio = None

class LiveMarketFeed:
    
    _INSTANCE = None
    
    
    def __new__(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = super().__new__(cls)
            
        return cls._INSTANCE
        
    
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        
        Logger.log("Initializing LiveMarket Feed!")
        self.app_access_token = ""
        self.is_valid = False
        self.fyersWS = None
        self.subscription_scripts = []
        self.last_update_recieved_time = None
        self.__forward_socket_url = None
        self.__forward_socket = None
        self.__forward_socket_event = Constants.LIVE_MARKET_FEED_FORWARD_EVENT_NAME
        self.feed_handler_func = None
        
        try:
            app_access_token = MainUtil.getAppAccessToken()
            if app_access_token  == "":
                Logger.log("Empty app access token received.")
                return
            self.app_access_token = app_access_token          
        
        except Exception as e:
            Logger.log("Error obtaining the app keys from file", e, type=LogType.ERROR)
            
    def setSubscriptionScripts(self, script_list):
        self.subscription_scripts = script_list
    
    def addSubscriptionScripts(self, script_list):
        self.fyersWS.subscribe(script_list)

    def setForwardSocketUrl(self, url):
        self.__forward_socket_url = url
        
    def setForwardSocketEvent(self, event_name):
        self.__forward_socket_event = event_name  
        
    def setFeedHandler(self, handlerFunc):
        self.feed_handler_func = handlerFunc

    
    def start(self):
        if self.fyersWS is not None:
            print("LiveMarketFeed Already Started!")
            return      
        
        try:       
            self.fyersWS = data_ws.FyersDataSocket(
                access_token=self.app_access_token,         # Access token in the format "appid:accesstoken"
                log_path=str(Constants.DIR_LOGS),                # Path to save logs. Leave empty to auto-create logs in the current directory.
                litemode=False,                             # Lite mode disabled. Set to True if you want a lite response.
                # write_to_file=True,                       # Save response in a log file instead of printing it.
                reconnect=True,                             # Enable auto-reconnection to WebSocket on disconnection.
                on_connect=self.onopen,                          # Callback function to subscribe to data upon connection.
                on_close=self.onclose,                           # Callback function to handle WebSocket connection close events.
                on_error=self.onerror,                           # Callback function to handle WebSocket errors.
                on_message=self.onmessage                        # Callback function to handle incoming messages from the WebSocket.
            )

            # Establish a connection to the Fyers WebSocket
            self.fyersWS.connect()
        except Exception as e:
            Logger.log("Error starting the LiveMarketFeed!", e, type=LogType.ERROR)
            

    def onopen(self):
        """
        Callback function to subscribe to data type and symbols upon WebSocket connection.

        """
        # Specify the data type and symbols you want to subscribe to
        data_type = "SymbolUpdate"
        
        Logger.log("LiveMarketFeed connection opened successfully")
    
            

        # Subscribe to the specified symbols and data type
        self.fyersWS.subscribe(symbols=self.subscription_scripts, data_type=data_type)

        # Keep the socket running to receive real-time data
        self.fyersWS.keep_running()
        
            
        if self.__forward_socket_url is not None:
            Logger.log("Connecting to forward socket!")
            # TODO: Connect to the socket
            self.__forward_socket = SocketUtility(self.__forward_socket_url)
            


    def handle_feed(self, message):
        """
        Handles market feed.
        """
        
          
        """
        SAMPLE MESSAGE:
        
        {'ltp': 50343.7,
        'prev_close_price': 50988.8,
        'ch': -645.1,
        'chp': -1.27,
        'exch_feed_time': 1736143438,
        'high_price': 51026.1,
        'low_price': 50193.1,
        'open_price': 50990.65,
        'type': 'if',
        'symbol': 'NSE:NIFTYBANK-INDEX'}
        """
        
        if self.__forward_socket_url is not None:
            self.send_message_to_forward_socket(message)


    def onmessage(self, message):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        self.last_update_recieved_time = datetime.now()
        self.handle_feed(message)

    def onerror(self, message):
        """
        Callback function to handle WebSocket errors.

        Parameters:
            message (dict): The error message received from the WebSocket.


        """
        print("Error:", message)


    def onclose(self, message):
        """
        Callback function to handle WebSocket connection close events.
        """
        print("Connection closed:", message)

    def is_forward_socket_connected(self):
        return self.__forward_socket.connected
    
    def send_message_to_forward_socket(self, message):
        """Send a message to the the forward socket server."""       
        try:
            self.__forward_socket.emit(self.__forward_socket_event, {'message': message})
            print(f"Message sent: {message}")
            pass
        except Exception as e:
            print(f"Error sending message: {e}")
     
