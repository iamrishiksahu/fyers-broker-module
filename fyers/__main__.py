from .authentication.Broker import Broker
from pathlib import Path
from .utils.Logger import Logger
from datetime import datetime
from .historicalDataDownloader import HistoricalDataDownloader

if __name__ == "__main__":

    broker = Broker.getInstance()
    if broker is None:
        print("Oops, broker could not be initialized")
    else:
        
        hdl = HistoricalDataDownloader(broker)
        hdl.setScripts([
            "NSE:NIFTY50-INDEX",
        ])
        
        startDate = "2025-01-01"
        endDate = "2025-01-04"
        timeframe = "1D"
        hdl.downloadData(startDate, endDate, timeframe)
        

        
        