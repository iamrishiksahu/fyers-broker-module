from utils.MainUtil import MainUtil
from utils.Logger import Logger, LogType
from utils.Constants import Constants
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime

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
        self.__forward_socket_event = "LiveMarketFeed"
        self.__sio = None
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
            

    # Create a Socket.IO client

    #Define event handlers
    # @sio.event
    # def connect():
    #     print("Connected to server.")

    #     # Emit data to a specific event
    #     sio.emit('custom_event', {'message': 'Hello, Server!', 'user': 'Alice'})

    # @sio.on('custom_response')
    # def on_custom_response(data):
    #     print("Received response:", data)

    # @sio.event
    # def disconnect():
    #     print("Disconnected from server.")

    # # Connect to the server
    # sio.connect('http://localhost:5000')

    # # Keep the connection alive
    # sio.wait()

    
    
    def onopen(self):
        """
        Callback function to subscribe to data type and symbols upon WebSocket connection.

        """
        # Specify the data type and symbols you want to subscribe to
        data_type = "SymbolUpdate"
        
        Logger.log("LiveMarketFeed connection opened successfully")
        
        if self.__forward_socket_url is not None:
            Logger.log("Connecting to forward socket!")
            # TODO: Connect to the socket
            # sio = socketio.Client()
            # self.sio = sio
            
            

        # Subscribe to the specified symbols and data type
        self.fyersWS.subscribe(symbols=self.subscription_scripts, data_type=data_type)

        # Keep the socket running to receive real-time data
        self.fyersWS.keep_running()

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
        

        """ 'if' means Index Feed & 'sf' means Symbol Feed"""
        if message['type'] == 'if' or message['type'] == 'sf':
            self.feed_handler_func(message)
    

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


   