from pymongo import MongoClient
from contextlib import contextmanager
from typing import Optional, Generator
from .ConfigManager import ConfigManager

class MongoDBManager:
    _instance = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls, *args, **kwargs):

        config = ConfigManager()
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
            cls._client = MongoClient(config.get_connection_string(), maxPoolSize=50)
        return cls._instance
    
    @classmethod
    @contextmanager
    def get_db(cls) -> Generator:
        config = ConfigManager()

        if cls._instance is None:
            MongoDBManager()
            
        try:
            db = cls._client[config.get_database_name()]
            cls._client.admin.command('ping')
            yield db
        except Exception as e:
            print(f"MongoDB Error: {e}")
            raise
