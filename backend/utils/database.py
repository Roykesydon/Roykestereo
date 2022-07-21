import os

import pymongo

from .config import get_env


def get_connection() -> pymongo.mongo_client.MongoClient:
    # uri = f"mongodb://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}"
    # uri = f"mongodb://root:pass@192.168.100.158:27119"
    env_dict = get_env()
    uri = f"mongodb://{env_dict['DB_USERNAME']}:{env_dict['DB_PASSWORD']}@{env_dict['DB_HOST']}"
    client = pymongo.MongoClient(uri)
    return client
