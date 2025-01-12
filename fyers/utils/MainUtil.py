import os
import hashlib
from pathlib import Path
from .FileUtility import FileUtility
from .Logger import Logger

class MainUtil:
    
    @staticmethod
    def getSHA256Hash(data):
        # Create a SHA-256 hash object
        sha256_hash = hashlib.sha256()

        # Update the hash object with the bytes of the string
        sha256_hash.update(data.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hex_digest = sha256_hash.hexdigest()
        return hex_digest

    
    @staticmethod
    def readFile(file_path):
        return MainUtil.execute(FileUtility.readFile, file_path)
    
    @staticmethod
    def deleteFile(file_path):
       return MainUtil.execute(FileUtility.deleteFile,file_path)
            
    @staticmethod
    def writeFile(file_path, data):   
        return MainUtil.execute(FileUtility.writeFile, file_path, data)
                
    @staticmethod
    def appendFile(file_path, data):   
        return MainUtil.execute(FileUtility.appendFile, file_path, data)
            
    @staticmethod
    def createDirectoryIfNotExists(file_path):
        return MainUtil.execute(FileUtility.createDirectoryIfNotExists, file_path)
    @staticmethod
    def checkIfDirectoryExists(file_path):
        return MainUtil.execute(FileUtility.checkIfDirectoryExists, file_path)
    
    @staticmethod
    def checkIfFileExists(file_path):
        return MainUtil.execute(FileUtility.checkIfFileExists, file_path)
    
    @staticmethod
    def execute(func, *args, **kwargs):
        res = func(*args, **kwargs)
        if res["log"] is not None:
            Logger.log(res["log"])
        return res["data"]
