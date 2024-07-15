# import library
import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import uvicorn.config
import platform

#import module
from module import get_readme_gitapi as readme
from module import logging as log
from module import generate_db as gdb

class FASTAPI_SERVER:
    
    def __init__(self):
        self.OWNER_NAME = "Tyranno-Rex"

        # FastAPI 서버 설정
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # MongoDB 연결
        # RELEASE: mongodb://root:1234@mongodb-container/
        # DEBUG: localhost:27017

        # 운영 체제를 확인하여 디버그 모드와 릴리즈 모드를 설정합니다.
        current_os = platform.system()
        print("=====================================")
        print("OS: ", current_os)
        if current_os == 'Windows':
            print("DEBUG")
            self.client = MongoClient('localhost', 27017)
        elif current_os == 'Linux':
            print("RELEASE")
            self.client = MongoClient('mongodb://root:1234@mongodb-container/')
        else:
            print("OS not supported")
            exit(1)
        print("=====================================")
        print("MongoDB Connection")
        try:
            self.client.admin.command('ismaster')
            print('Connected to MongoDB')
        except ConnectionFailure:
            print('MongoDB server not available')
        # readme 데이터베이스
        self.git_repo_mongodb = self.client['github_repo']
        print("=====================================")

        # portfolio 데이터베이스
        self.portfoilo = self.client['portfolio']
        self.repos = self.portfoilo['repo-positions']
        self.categories = self.portfoilo['category-positions']
        self.repo_category = self.portfoilo['repo-category']

        # FastAPI 이벤트 설정
        self.app.add_event_handler("startup", self.startup_event)
        
        # FastAPI 라우터 설정
        self.router = APIRouter()
        self.router.add_api_route('/readme', endpoint=self.get_all_repo_readme, methods=['GET'])
        self.router.add_api_route('/repo-category', endpoint=self.get_all_repo_category, methods=['GET'])
        self.router.add_api_route('/generate-database', endpoint=self.generate_database, methods=['GET'])
        self.app.include_router(self.router)
        
        print("=====================================")
        # GitHub API 토큰
        import os
        print("project path: ", os.getcwd())
        
        if current_os == "Windows":
            # Windows의 ./back-end/main/git-token.txt 파일을 읽는다.
            print("DEBUG")
            self.token = open("./back-end/main/git-token.txt", "r").read().strip()
        else:
            print("RELEASE")
            # ubuntu의 /home/ubuntu/git-token 파일을 읽는다.
            try:
                self.token = open('/home/ubuntu/git-token.txt', 'r').read().strip()
            except FileNotFoundError:
                self.token = "null"
        print("=====================================")

    async def startup_event(self):
        log.access_log()

    def get_all_repo_readme(self):
        repo_all_list = readme.get_all_repos(self.token)
        repo_all_list = readme.get_readme(repo_all_list, self.OWNER_NAME, self.token)
        return repo_all_list
    
    def get_all_repo_category(self):
        repos = self.repos.find()
        categories = self.categories.find()
        repo_category = self.repo_category.find()
        json_repo_category = {'repos': [], 'categories': [], 'repo-category': []}
        
        for repo in repos:
            json_repo_category['repos'].append({'repo': repo['repo'], 'position': repo['position']})
        for category in categories:
            json_repo_category['categories'].append({'category': category['category'], 'position': category['position']})
        for rc in repo_category:
            json_repo_category['repo-category'].append({'repo': rc['repo'], 'categories': rc['categories']})
        return json_repo_category
    
    def generate_database(self):
        gdb.generate_database(uvicorn.config.LOG_LEVEL)
        return {"status": "success"}

fastapi_server = FASTAPI_SERVER()
app = fastapi_server.app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
