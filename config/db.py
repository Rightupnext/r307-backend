
from mongoengine import connect, get_connection
import os, sys
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def init_db():
    try:
        connect(host=MONGO_URI)
        client = get_connection()
        client.admin.command("ping")
        print("? MongoDB connected")

        parsed = urlparse(MONGO_URI)
        db_name = parsed.path.lstrip('/')
        print(f"?? Database: {db_name}")
        
    except Exception as e:
        print("? DB connection failed:", e)
        sys.exit(1)
