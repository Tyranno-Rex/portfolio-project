import platform        
import datetime
from pymongo import MongoClient
import logging
import uvicorn
import datetime
import pytz

# Save the log to the MongoDB
# Timestamp: UTC time + 9 hours (KST) => Asia/Seoul timezone
# Logs is saved by date (e.g., 2021-08-01)
def save_log_to_mongodb(log_message, client):
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        utc_now = datetime.datetime.now(datetime.timezone.utc)

        # KST = UTC + 9 hours / korea timezone
        kst = pytz.timezone('Asia/Seoul')
        kst_now = utc_now.astimezone(kst)

        log_entry = {
            "timestamp": kst_now,
            "message": log_message
        }
        
        log_db = client['log']
        log = log_db[today]
        log.insert_one(log_entry)
    except Exception as e:
        print(f"Failed to save log to MongoDB: {e}")

# Access log
# Save the access log to the MongoDB -> Log data is terminal output
def access_log(client):
    logger = logging.getLogger('uvicorn.access')
    console_formatter = uvicorn.logging.ColourizedFormatter("{asctime} - {message}", style="{", use_colors=True)
    
    # MongoDB Handler
    class MongoDBHandler(logging.Handler):
        def emit(self, record):
            log_message = self.format(record)
            save_log_to_mongodb(log_message, client)

    mongodb_handler = MongoDBHandler()
    mongodb_handler.setFormatter(console_formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(mongodb_handler)