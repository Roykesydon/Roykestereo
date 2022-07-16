import pymongo

from .config import get_env


def get_connection() -> pymongo.mongo_client.MongoClient:
    env_dict = get_env()
    uri = f"mongodb://{env_dict['DB_USERNAME']}:{env_dict['DB_PASSWORD']}@192.168.100.158:27119"
    client = pymongo.MongoClient(uri)
    return client
