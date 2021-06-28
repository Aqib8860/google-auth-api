from pymongo import MongoClient
from server.local_settings import DBInfo
import traceback

'''
DATABASE CONNECTION
'''

def connect() -> MongoClient: 
    return MongoClient(DBInfo.get_url())

class Connect():
    def __init__(self):
        self.client = connect()
        
    def __enter__(self):
        return self.client
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        traceback.extract_tb(exc_tb)
        self.client.close()
