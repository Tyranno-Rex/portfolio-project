
from pymongo import MongoClient


def save_repo_data_in_mongo(repo_all_list, current_os):
    if current_os == 'Windows':
        client = MongoClient('mongodb://localhost:27017/')
    elif current_os == 'Linux':
        client = MongoClient('mongodb://root:1234@mongodb-container/')
    else:
        print("OS not supported")
        exit(1)
    
    
    db = client['github_repo']
    collection = db['repo']
    collection.delete_many({})
    collection.insert_many(repo_all_list)
    client.close()
    return True