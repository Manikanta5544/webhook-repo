from pymongo import MongoClient, ASCENDING, DESCENDING
from config import MONGO_URI, DB_NAME, EVENTS_COLLECTION

# Connect to MongoDB (NO ping at import time)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client[DB_NAME]
events_collection = db[EVENTS_COLLECTION]

# Index for deduplication
events_collection.create_index(
    [("request_id", ASCENDING)],
    unique=True
)

# Index for fast time-based queries
events_collection.create_index(
    [("timestamp", DESCENDING)]
)
