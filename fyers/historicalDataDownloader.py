# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel
from datetime import datetime
import json
from datetime import datetime, timedelta
import time
from .utils.MainUtil import MainUtil
from .utils.Constants import Constants


# Create a datetime object

class HistoricalDataDownloader:
    
    def __init__(self, broker):
        self.broker = broker
        self.scripts = []


    def perform(self,frmdt, todt, scrpt, timeframe="1D"):
        
        
        fromDatestr = frmdt
        toDatestr = todt
        fromDateObj = datetime.strptime(fromDatestr, "%Y-%m-%d")
        toDateObj = datetime.strptime(toDatestr, "%Y-%m-%d")

        # Convert to Unix timestamp
        fromTimestamp = str(int(fromDateObj.timestamp()))
        toTimestamp = str(int(toDateObj.timestamp()))


        data = {
            "symbol": scrpt,
            "resolution": timeframe,
            "date_format":"0",
            "range_from":fromTimestamp,
            "range_to":toTimestamp,
            "cont_flag":"1"
        }

        response = self.broker.history(data=data)

        if response['code'] != 200:
            # Some error occurred
            print(response)
            

        histData = response['candles']

        # Convert data into string
        newHistData = ""
        for item in histData:
            date = datetime.fromtimestamp(int(item[0])).strftime('%Y-%m-%d %H:%M')
            item[0] = date
            newHistData += ",".join([str(a) for a in item]) + "\n"
            
        return newHistData

    def setScripts(self, scripts):
        
        self.scripts = scripts

    def downloadData(self, startDate, endDate, timeframe = "1D"):
        

        for script in self.scripts:
            fromDt = startDate
            toDt = self.get_date_after_n_days(fromDt, 99)
            if toDt > endDate : toDt = endDate
            filename = script.split(":")[1] + "(" + timeframe + ") [" + f"{startDate} -  {self.get_date_after_n_days(endDate, -1)}" + "].csv"
            print("CURRENT: " + script)
            data = ""
            
            while toDt <= endDate and fromDt <= toDt:
                print(fromDt + "  " + toDt )  
                data += self.perform(fromDt, toDt, script, timeframe)
                time.sleep(2)
                    
                fromDt = self.get_date_after_n_days(toDt, 1)
                toDt = self.get_date_after_n_days(fromDt,99) 
                if toDt > endDate : toDt = endDate
                        

            
            MainUtil.writeFile(Constants.DIR_ROOT.joinpath("resources/historical_data").joinpath(filename), data)
        
            
    def get_date_after_n_days(self, date_str, n):

        # Convert the input string to a datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Add n days using timedelta
        new_date = date_obj + timedelta(days=n)
        
        # Return the resulting date as a string in the same format
        return new_date.strftime("%Y-%m-%d")


        
            