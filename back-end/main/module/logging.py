import platform        
import datetime
from pymongo import MongoClient
import logging
import uvicorn
import datetime
import pytz

def save_log_to_mongodb(log_message):
    try:
        # 10.0.0.199 / 10.0.1.195 은 health check용 IP -> 로그 저장하지 않음
        if "10.0.0.199" in log_message or "10.0.1.195" in log_message:
            return

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        utc_now = datetime.datetime.now(datetime.timezone.utc)

        # KST = UTC + 9 hours / korea timezone
        kst = pytz.timezone('Asia/Seoul')
        kst_now = utc_now.astimezone(kst)

        log_entry = {
            "timestamp": kst_now,
            "message": log_message
        }

        current_os = platform.system()
        if current_os == 'Windows':
            PASSWORD = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-mongo-token.txt", "r").read().strip()
        else:
            PASSWORD = open("/app/mongo-token.txt", "r").read().strip()
        client = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")
        
        log_db = client['log']
        log = log_db[today]
        log.insert_one(log_entry)
        client.close()

    except Exception as e:
        print(f"Failed to save log to MongoDB: {e}")

def access_log():
    logger = logging.getLogger('uvicorn.access')
    console_formatter = uvicorn.logging.ColourizedFormatter("{asctime} - {message}", style="{", use_colors=True)
    
    # MongoDB 핸들러
    class MongoDBHandler(logging.Handler):
        def emit(self, record):
            log_message = self.format(record)
            save_log_to_mongodb(log_message)

    mongodb_handler = MongoDBHandler()
    mongodb_handler.setFormatter(console_formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(mongodb_handler)