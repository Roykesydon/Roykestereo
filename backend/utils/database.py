import os

import pymongo


def get_connection() -> pymongo.mongo_client.MongoClient:
    uri = f"mongodb://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}"
    client = pymongo.MongoClient(uri)
    return client
