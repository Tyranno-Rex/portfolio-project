

import base64
from requests import get
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import uvicorn

#import file
from module import get_readme_gitapi as readme

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
        self.client = MongoClient('localhost', 27017)
        try:
            self.client.admin.command('ismaster')
            print('Connected to MongoDB')
        except ConnectionFailure:
            print('MongoDB server not available')
        # readme 데이터베이스
        self.git_repo_mongodb = self.client['github_repo']
        
        # portfolio 데이터베이스
        self.portfoilo = self.client['portfolio']
        self.repos = self.portfoilo['repo-positions']
        self.categories = self.portfoilo['category-positions']
        self.repo_category = self.portfoilo['repo-category']
        # FastAPI 라우터 설정
        self.router = APIRouter()
        self.router.add_api_route('/readme', endpoint=self.get_all_repo_readme, methods=['GET'])
        self.router.add_api_route('/repo-category', endpoint=self.get_all_repo_category, methods=['GET'])
        self.app.include_router(self.router)
        # GitHub API 토큰
        self.token = open("C:/Users/admin/project/portfolio-project/back-end/database-server/api/database/git-token.txt", "r").read().strip()

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

if __name__ == "__main__":
    fastapi_server = FASTAPI_SERVER()
    uvicorn.run(fastapi_server.app, host="0.0.0.0", port=8000)
    pass