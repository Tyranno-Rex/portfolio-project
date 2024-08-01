#---------------------------------------------------------------------------------------------------#
# THIS IS THE MAIN FILE FOR THE FASTAPI SERVER THAT RUNS THE BACKEND OF THE PORTFOLIO PROJECT.      #
# Automated Update Funtion and Client Request Function are implemented in this file.                #
#                                                                                                   #
# __init__ Function:                                                                                #
# 1. Fastapi middleware setting                                                                     #
# 2. MongoDB Connection                                                                             #
# 3. Access Token Setting                                                                           #
# 4. Git Token Setting                                                                              #
# 5. FastAPI Event Setting                                                                          #
# 6. FastAPI Router Setting                                                                         #
# 7. FastAPI Server Setting                                                                         #
#                                                                                                   #
# check_server Function:                                                                            #
# 1. Simple check if the server is running                                                          #
# 2. return JSONResponse(status_code=200, content={"message": "Server is running"})                 #
#                                                                                                   #
# startup_event Function:                                                                           #
# 1. Log the server startup And all termninal logs                                                  #
# 2. No return value, just log the server startup                                                   #
#                                                                                                   #
# get_all_repo_readme Function:                                                                     #
# 1. Main Funciont that update all the readme data through the github api and save it in the        #
# database (MongoDB)                                                                                #
# 2. return JSONResponse(status_code=200, content={"message": "Readme data saved successfully"})    #
#                                                                                                   #
# generate_database Function:                                                                       #
# 1. Generate the rendering data from the database and save it in the database                      #
# 2. return JSONResponse(status_code=200, content={"message": "Database generated successfully"})   #
#                                                                                                   #
# get_all_repo_category Function:                                                                   #
# 1. Get all the repo category data from the database                                               #
# 2. return all the repo category data that name and 3d position                                    #
#                                                                                                   #
# get_repo_info Function:                                                                           #
# 1. Get the Requested Repository Information from the database                                     #
# 2. return the requested repository information                                                    #
#                                                                                                   #
# Last Updated: 2024-08-01                                                                          #
#---------------------------------------------------------------------------------------------------#


# import library
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import uvicorn.config
import platform

#import module
from module import get_readme_gitapi as readme
from module import logging as log
from module import generate_db as gdb
from module import save_repo_data_in_mongo as saveInMongo
from module import get_database_info as db_info

class FASTAPI_SERVER:
    
    # Server Setting
    # 1. Fastapi middleware setting
    # 2. MongoDB Connection
    # 3. Access Token Setting
    # 4. Git Token Setting
    # 5. FastAPI Event Setting
    # 6. FastAPI Router Setting
    # 7. FastAPI Server Setting
    # Last Updated: 2024-08-01
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

        # 운영 체제를 확인
        self.current_os = platform.system()
        print("Environment: ", self.current_os)

        # MongoDB 연결
        try :
            print("=====================================")
            print("MongoDB Connection")
            if self.current_os == 'Windows':
                PASSWORD = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-mongo-token.txt", "r").read().strip()
            else:
                PASSWORD = open("/app/mongo-token.txt", "r").read().strip()
            
            print("Password: ", PASSWORD)
            self.client = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")
            try:
                self.client.admin.command('ismaster')
            except ConnectionFailure:
                print('MongoDB server not available')
            # readme 데이터베이스
            self.git_repo_mongodb = self.client['github_repo']

            # portfolio 데이터베이스
            self.portfoilo = self.client['portfolio']
            self.repos = self.portfoilo['repo-positions']
            self.categories = self.portfoilo['category-positions']
            self.repo_category = self.portfoilo['repo-category']
            print("MongoDB Connection Complete")
            print("=====================================")
        except Exception as e:
            print("MongoDB Connection Error: ", e)
            print("=====================================")

        # access-token 설정
        try :
            print("=====================================")
            print("Access Token Setting")
            if self.current_os == 'Windows':
                self.access_token = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-access-token.txt", "r").read().strip()
            else:
                self.access_token = open("/app/access-token.txt", "r").read().strip()
            print("Access Token: ", self.access_token)
            print("Access Token Setting Complete")
            print("=====================================")
        except Exception as e:
            print("Access Token Error: ", e)
            print("=====================================")

        # Git Token 설정
        try:
            print("=====================================")
            print("Token Setting")
            if self.current_os == 'Windows':
                print("DEBUG")
                self.token = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-git-token.txt", "r").read().strip()
            else:
                print("RELEASE")
                try:
                    self.token = open('/app/git-token.txt', 'r').read().strip()
                except FileNotFoundError:
                    self.token = "null"
            print("Token: ", self.token)
            print("Token Setting Complete")
            print("=====================================")
        except Exception as e:
            print("Token Error: ", e)
            print("=====================================")

        print("=====================================")
        print("FastAPI Server Setting")
        
        # FastAPI 이벤트 설정
        self.app.add_event_handler("startup", self.startup_event)
        
        # FastAPI 라우터 설정
        self.router = APIRouter()
        self.router.add_api_route('/', endpoint=self.check_server, methods=['GET'])
        self.router.add_api_route('/readme', endpoint=self.get_all_repo_readme, methods=['GET'])
        self.router.add_api_route('/repo-category', endpoint=self.get_all_repo_category, methods=['GET'])
        self.router.add_api_route('/generate-database', endpoint=self.generate_database, methods=['GET'])
        self.router.add_api_route('/get-repo-info', endpoint=self.get_repo_info, methods=['GET'])
        self.app.include_router(self.router)
        
        print("FastAPI Server Setting Complete")
        print("=====================================")

    # Simple check if the server is running
    # Last Updated: 2024-08-01
    # memeory leak test passed!
    async def check_server(self):
        return JSONResponse(status_code=200, content={"message": "Server is running"})

    # Log the server startup And all termninal logs
    # Last Updated: 2024-08-01
    # memeory leak test passed!
    async def startup_event(self):
        log.access_log(self.client)

    # Automation Function
    # Main Funciont that update all the readme data through the github api and save it in the database (MongoDB)
    # Last Updated: 2024-08-01
    # memeory leak test not passed...
    async def get_all_repo_readme(self, request: Request):
        access_token = request.query_params.get('access_token')

        if access_token != self.access_token:
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        else:
            repo_all_list = readme.get_all_repos(self.token)
            readme.get_readme(repo_all_list, self.OWNER_NAME, self.token, self.client)
            return JSONResponse(status_code=200, content={"message": "Readme data saved successfully"})

    # Automation Function
    # Generate the rendering data from the database and save it in the database
    # Last Updated: 2024-08-01
    # memeory leak test passed!
    async def generate_database(self, request: Request):
        access_token = request.query_params.get('access_token')
        print("Access Token: ", access_token)
        if access_token != self.access_token:
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        else :
            print("=====================================")
            print("===Generate Database===")
            gdb.generate_database(self.client)
            print("===Save Repository Data===")
            print("=====================================")
            return JSONResponse(status_code=200, content={"message": "Database generated successfully"})
    
    # Client Request Function
    # Get all the repo category data from the database
    # Last Updated: 2024-08-01
    # memeory leak test passed!
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

    # Client Request Function
    # Get the Requested Repository Information from the database
    # Last Updated: 2024-08-01
    # memeory leak test passed!
    async def get_repo_info(self, request: Request):
        repo = request.query_params.get('repo')
        if not repo:
            return JSONResponse(status_code=400, content={"error": "Repository name not provided"})
        repo_info = db_info.find_repo_data(repo, self.client)
        if not repo_info:
            return JSONResponse(status_code=404, content={"error": "Repository not found"})
        return JSONResponse(status_code=200, content=repo_info)


fastapi_server = FASTAPI_SERVER()
app = fastapi_server.app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
