import os
from .Constants import Constants
from datetime import datetime
from .FileUtility import FileUtility

class Logger:    
    
    LOG_FILEPATH = None
    
    @staticmethod
    def getLogFilename():
        if Logger.LOG_FILEPATH is None:
            time = datetime.today().timetuple()
            time_str = str(time[3]) + "-"+str(time[4])+"-"+str(time[5])
            date_time_str = str(datetime.today().date()) + " " + str(time_str)
            Logger.LOG_FILEPATH = Constants.DIR_LOGS.joinpath(date_time_str + ".txt")
            
        return Logger.LOG_FILEPATH
    
    @staticmethod
    def log(*args, sep=" ", end="\n"):
        """
            Args:
            *args: Positional arguments to log (similar to print()).
            sep (str): String inserted between arguments. Default is a single space.
            end (str): String appended after the last argument. Default is a newline.
            file: A file-like object to which the output is written. Default is sys.stdout.
            flush (bool): Whether to flush the output stream. Default is False.
            log_to_file (str): File path to log the output (appends to the file).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = sep.join(str(arg) for arg in args)
        print(message)
        message = str(message) + str(end)
        message = f"[{timestamp}] {message}"
        FileUtility.appendFile(Logger.getLogFilename(),message)
   