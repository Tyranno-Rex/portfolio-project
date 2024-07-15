import datetime
from pymongo import MongoClient
import logging
import uvicorn

def save_log_to_mongodb(log_message):
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        log_entry = {
            "timestamp": datetime.datetime.now(),
            "message": log_message
        }
        # if 
        # client = MongoClient('mongodb://root:1234@mongodb-container/')
                # 운영 체제를 확인하여 디버그 모드와 릴리즈 모드를 설정합니다.
        import platform
        
        current_os = platform.system()
        client = None
        if current_os == 'Windows':
            client = MongoClient('localhost', 27017)
        elif current_os == 'Linux':
            client = MongoClient('mongodb://root:1234@mongodb-container/')
        else:
            print("OS not supported")
        log_db = client['log']
        log = log_db[today]
        log.insert_one(log_entry)
        client.close()  # MongoDB 연결 종료
    except Exception as e:
        print(f"Failed to save log to MongoDB: {e}")

def access_log():
    logger = logging.getLogger('uvicorn.access')
    console_formatter = uvicorn.logging.ColourizedFormatter("{asctime} - {message}", style="{", use_colors=True)
    
    # 파일 핸들러
    # file_handler = logging.handlers.TimedRotatingFileHandler("./database", when='midnight', interval=1, backupCount=1)
    # file_handler.setFormatter(console_formatter)
    
    # MongoDB 핸들러
    class MongoDBHandler(logging.Handler):
        def emit(self, record):
            log_message = self.format(record)
            save_log_to_mongodb(log_message)

    mongodb_handler = MongoDBHandler()
    mongodb_handler.setFormatter(console_formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(mongodb_handler)