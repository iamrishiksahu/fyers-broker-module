from .HistoricalDataDownloader import HistoricalDataDownloader
from .Broker import Broker 
from .LiveMarketFeed import LiveMarketFeed

class Main:
    
    def __init__(self):
        pass
    
    def run(self):
        
        broker = Broker.getInstance()
        if broker is None:
            print("Oops, broker could not be initialized")
            return
    
        # Sample implementation of downloading historical data for NIFTY 50
        # hdl = HistoricalDataDownloader(broker)
        # hdl.setScripts([
        #     "NSE:NIFTY50-INDEX",
        # ])
        
        # startDate = "2025-01-01"
        # endDate = "2025-01-04"
        # timeframe = "1D"
        # hdl.downloadData(startDate, endDate, timeframe)
        
        # You can write your own implementation here
        
        
        lmf = LiveMarketFeed()
        lmf.setSubscriptionScripts(["NSE:NIFTY50-INDEX" , "NSE:NIFTYBANK-INDEX"])
        lmf.start()
        
            
