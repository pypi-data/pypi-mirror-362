import sys
import logging
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ASyncMongoClient:
    """
    An Async Utility to work with MonogDB
    """
    def __init__(self, mongo_uri:str=None):
        try:
            self.mongo_client = AsyncIOMotorClient(
                mongo_uri,     
                maxPoolSize=50,
                minPoolSize=5,
                maxConnecting=10
            )
        except Exception as e:
                logging.error(f"MongoDB client init failed: {e}")
                self.mongo_client = None


    async def find_one_record(self, database_name:str=None, collection_name:str=None, filter_query:dict=None, filter_fields:dict=None):
        """
        Method to fetch company record from financial collection
        """
        if self.mongo_client is None:
            logging.error("Mongo Client Not active!")
            return None

        try:
            collection = self.mongo_client[database_name][collection_name]
            results = await collection.find_one(filter_query, filter_fields)
            return results
        
        except Exception as e:
            logging.error(f"ERROR AsyncMongoClient (find_one_record): {e}")
            return None