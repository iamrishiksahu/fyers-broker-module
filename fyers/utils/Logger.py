import os
from .Constants import Constants
from datetime import datetime
from .FileUtility import FileUtility
from enum import Enum
from pathlib import Path

class LogType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Logger:    
    
    LOG_FILEPATH = None
    MAX_LOG_COUNT_PER_FILE = 1000
    TOTAL_LOG_COUNT = 0
    CURRENT_FILE_LOG_COUNT = 0
    
    @staticmethod
    def getLogFilename():        
            
        if Logger.LOG_FILEPATH is None:
            time = datetime.today().timetuple()
            time_str = str(time[3]) + "-"+str(time[4])+"-"+str(time[5])
            date_time_str = str(datetime.today().date()) + " " + str(time_str)
            Logger.LOG_FILEPATH = Constants.DIR_LOGS.joinpath(date_time_str + ".log")
            
        elif Logger.CURRENT_FILE_LOG_COUNT > Logger.MAX_LOG_COUNT_PER_FILE:
            """
                When the log file count exceeds the max limit,
                we want to add further logs in a separate file.
            """
            Logger.CURRENT_FILE_LOG_COUNT = 1
            Logger.LOG_FILEPATH = Path(str(Logger.LOG_FILEPATH).split(".log")[0].join(f"_{Logger.TOTAL_LOG_COUNT%Logger.MAX_LOG_COUNT_PER_FILE}.log"))
            
        return Logger.LOG_FILEPATH
    
    @staticmethod
    def log(*args, type=LogType.INFO, sep=" ", end="\n"):
        """
            Args:
            *args: Positional arguments to log (similar to print()).
            type (LogType): Type of log 
            sep (str): String inserted between arguments. Default is a single space.
            end (str): String appended after the last argument. Default is a newline.
        """
        Logger.CURRENT_FILE_LOG_COUNT += 1
        Logger.TOTAL_LOG_COUNT += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = sep.join(str(arg) for arg in args)
        print(message)
        message = str(message) + str(end)
        message = f"[{timestamp}] {type} {message}"
        FileUtility.appendFile(Logger.getLogFilename(),message)
   

    
    