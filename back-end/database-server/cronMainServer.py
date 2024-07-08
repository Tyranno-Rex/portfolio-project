


import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware

class FASTAPI_CRON_SERVER:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.client = MongoClient('localhost', 27017)
        self.git_repo_mongodb = self.client['github_repo']
        self.router = APIRouter()
        self.router.add_api_route('/crawling', endpoint=self.crawling_main, methods=['GET'])
        self.app.include_router(self.router)
    def crawling_get_README(self, url):
        git_repo = requests.get(url)
        git_soup = BeautifulSoup(git_repo.text, 'html.parser')
        git_readme = git_soup.select_one("article.markdown-body.entry-content.container-lg").text.strip()
        project_crawling_info = git_readme.split('Project Crawling')[1].strip()
        project_name = project_crawling_info.split('PROJECT_NAME : ')[1].split('\n')[0]
        project_description = project_crawling_info.split('PROJECT_DESCRIPTION : ')[1].split('\n')[0]
        project_url = project_crawling_info.split('PROJECT_URL : ')[1].split('\n')[0]
        project_complete_status = project_crawling_info.split('PROJECT_COMPLETION_STATUS : ')[1].split('\n')[0]
        multi_projects = project_crawling_info.split('PROJECT_MULTI : ')[1].split('\n')[0]
        project_category = project_crawling_info.split('PROJECT_SUBPROJECT : ')[1].split('\n')[0]
        sub_project = project_category.split(', ')
        
        subproject_crawling_data = []
        if (multi_projects == 'TRUE'):
            for i in range(len(sub_project)):
                sub_project[i] = sub_project[i].strip()[1:-1]
                subproject_crawling_data.append(self.crawling_get_README(sub_project[i])) 
        category = project_crawling_info.split('PROJECT_CATEGORY : ')[1].split('\n')[0]
        category = category.split(', ')
        return {
                "project_name": project_name, 
                "project_description": project_description, 
                "project_url": project_url, 
                "project_complete_status": project_complete_status, 
                "multi_projects": multi_projects, 
                "sub_project": sub_project,
                "category": category,
                "subproject_crawling_data": subproject_crawling_data
        }
    def crawling_main(self):
        git_url = "https://github.com/Tyranno-Rex?tab=repositories"
        response = requests.get(git_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        repos = []
        for i, repo in enumerate(soup.select("h3 > a")):
            repo_url = f"https://github.com{repo['href']}"
            repos.append({"name": repo.text.strip(), "url": repo_url})
        
        for i in range(len(repos)):
            if (i == 0):
                project_crawling_info = self.crawling_get_README(repos[i]["url"])
                return project_crawling_info

    
if __name__ == "__main__":
    server = FASTAPI_CRON_SERVER()
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8001)