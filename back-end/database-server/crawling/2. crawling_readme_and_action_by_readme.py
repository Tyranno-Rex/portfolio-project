


import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware
import random
import time

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


    def get_git_repo_with_retries(self, url, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
                if attempt == 0:
                    print(f"Attempt {attempt} fetched {url}.")
                else:
                    print(f"Attempt {attempt} fetched {url}. Retrying in {wait_time:.2f} seconds...")
                git_repo = requests.get(url)
                time.sleep(wait_time)
                git_repo.raise_for_status()  # Raise an exception for HTTP errors
                return git_repo
            except requests.RequestException as e:
                attempt += 1
                print(f"Failed to fetch the URL: {e}")
        raise Exception(f"Failed to fetch the URL after {max_retries} attempts")

    def get_readme_with_retries(self, soup, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
                if attempt == 0:
                    print(f"Attempt {attempt} parsed the HTML.")
                else:
                    print(f"Attempt {attempt} parsed the HTML. Retrying in {wait_time:.2f} seconds...")
                git_readme_element = soup.select_one("article.markdown-body.entry-content.container-lg")
                time.sleep(wait_time)
                if git_readme_element:
                    return git_readme_element.text.strip()
                else:
                    raise Exception("README element not found")
            except Exception as e:
                attempt += 1
                print(f"Failed to parse the HTML: {e}")
        raise Exception(f"Failed to parse the HTML after {max_retries} attempts")

    def crawling_get_README(self, url):
        # Fetch the repository page with retries
        # git_repo = self.get_git_repo_with_retries(url)
        # Parse the HTML content with BeautifulSoup
        # git_soup = BeautifulSoup(git_repo.text, 'html.parser')
        # Extract the README text with retries
        # git_readme = self.get_readme_with_retries(git_soup)
        git_repo = requests.get(url)
        git_soup = BeautifulSoup(git_repo.text, 'html.parser')
        print(git_soup)
        git_readme = git_soup.select_one("article.markdown-body.entry-content.container-lg").text.strip()
        print(git_readme)

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
        
        crawling_data = []
        for i in range(len(repos)):
            # if (repos[i]["name"] == "portfolio-project" or repos[i]["name"] == "BE-study"):
            # if (repos[i]["name"] == "portfolio-project"):
            if (repos[i]["name"] == "BE-study"):
                crawling_data.append(self.crawling_get_README(repos[i]["url"]))

        # self.git_repo_mongodb['crawling_data'].insert_many(crawling_data)
        return {"crawling_data": crawling_data}
if __name__ == "__main__":
    server = FASTAPI_CRON_SERVER()
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8001)