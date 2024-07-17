from bson import ObjectId
from pymongo import MongoClient
import platform

def find_repo_data(repo_name):

    current_os = platform.system()
    if current_os == 'Windows':
        client = MongoClient('mongodb://localhost:27017/')
    elif current_os == 'Linux':
        client = MongoClient('mongodb://root:1234@mongodb-container/')
    else:
        print("OS not supported")
        exit(1)
    
    db = client['portfolio']
    repos = db['database']

    # /가 존재하면 /기준 뒤에 있는 것을 repo_name으로 설정
    if '/' in repo_name:
        repo_name = repo_name.split('/')[1]
    
    repo = repos.find_one({"name": repo_name})
    response = {
        "name": repo.get('name', 'default_name'),
        "url": repo.get('url', 'default_url'),
        "readme": repo.get('readme', 'default_readme'),
        "description": repo.get('description', 'default_description'),
        "complete_status": repo.get('complete_status', 'default_status'),
        "multi": repo.get('multi', 'default_multi'),
        "category": repo.get('category', 'default_category'),
        "subproject": repo.get('subproject', 'default_subproject')
    }

    client.close()
    return response


