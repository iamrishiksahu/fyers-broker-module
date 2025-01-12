# Documentation
This document serves as the documentation for Fyers Trading Module application.

## Use cases of this project
Here are some of the major use-cases of this application:

- Algo Trading
- Accessing Live Market Feed
- Donwloading Historical Data
- Data Analysis
- Backtesting
- Account Analysis

## Necessary Steps:
The file `fyers/Main.py` works as the entry point of the application.

the `run()` method is by convention used to initialize the SDK and the Broker module.

Starting boilerplate for the `Main.py` file:
```bash
from .HistoricalDataDownloader import HistoricalDataDownloader
from .Broker import Broker 

class Main:
    
    def __init__(self):
        pass

    def myImplementation():
        pass
    
    def run(self):
        
        broker = Broker.getInstance()
        if broker is None:
            print("Oops, broker could not be initialized")
            return
        
        # You can write your own implementation from here            
        self.myImplementation()
```

# Elaborated docs on use cases
From here you can find the elaborated docs based on each use-case. Feel free to use this project for any of your own use cases.

## Downloading Historical Data
You can download historical OHLC of multiple timeframes.
Support Timeframes: 1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 120, 180, 240, 1D

The result will be obtained in a `CSV` file under the directory: `fyers\outputs\historical_data`

Check: `fyers\utils\Constants.py` for any change in directory.

Sample code:
```bash
def myImplementation():

    hdl = HistoricalDataDownloader(broker)

    # Get the exact script name from the fyers web app.
    hdl.setScripts([
        "NSE:NIFTY50-INDEX",
        # Add more if you want
    ])
    
    # Dates has to be entered in YYYY-MM-DD format only
    startDate = "2025-01-01" 
    endDate = "2025-01-04"
    timeframe = "1D"

    hdl.downloadData(startDate, endDate, timeframe)

```

**Limits**
There is not limit of the data duration for the supported timeframes. Limits by Fyers API has been handled gracefully.
[Visit here for more details]("https://myapi.fyers.in/docsv3#tag/Data-Api/paths/~1DataApi/post")
