import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "webhook_db"
EVENTS_COLLECTION = "events"

# Flask
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_ENV = os.getenv("FLASK_ENV", "development")
