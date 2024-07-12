import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# github의 닉네임을 받는다
def get_github_id():
    github_id = input("Github ID를 입력하세요: ")
    return github_id



# github의 닉네임을 받아서 해당 유저의 저장소를 크롤링한다
def crawling(github_id):

    github_url = "github.com"
    github_personal_url = f"https://{github_url}/{github_id}?tab=repositories"
    response = requests.get(github_personal_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for i, repo in enumerate(soup.select("h3 > a")):
        repo_url = f"https://{github_url}{repo['href']}"
        repos.append({"name": repo.text.strip(), "url": repo_url})
    
    # 해당 주소의 모든 저장소의 세부 정보(readme, 주요 언어, commit 횟수, star 수, fork 수)를 크롤링한다




    response2 = requests.get(repos[1]["url"])
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    readme = soup2.select_one("article.markdown-body.entry-content.container-lg").text.strip()

    print(repos[1]["name"])
    
    client = MongoClient('192.168.3.3', 27018)
    try:
        # 연결 테스트
        client.admin.command('ismaster')
        print('Connected to MongoDB')
    except ConnectionFailure:
        print('MongoDB server not available')

    
    Project_Crawling_info = readme.split('Project Category - for crawling')[1].strip()
    print(Project_Crawling_info)
    ProjectCompleteStatus = Project_Crawling_info.split('PROJECT COMPLETION STATUS : ')[1].split('\n')[0]
    MultiProjects = Project_Crawling_info.split('MULIT PROJECTS : ')[1].split('\n')[0]
    
    print(ProjectCompleteStatus)
    print(MultiProjects)
    subProject = []
    category = []
    if MultiProjects == 'TRUE':
        # SUB PROJECTS : 'https://github.com/Tyranno-Rex/BE-study/tree/main/study-database', 'https://github.com/Tyranno-Rex/BE-study/tree/main/study-os/This-is-the-Linux', 'https://github.com/Tyranno-Rex/BE-study/tree/main/study-server'
        ProjectCategory = Project_Crawling_info.split('SUB PROJECTS : ')[1].split('\n')[0]
        subProject = ProjectCategory.split(', ')
        print(subProject)
    else:
        ProjectCategory = Project_Crawling_info.split('CATEGORY : ')[1].split('\n')[0]
        category = ProjectCategory.split(', ')
        print(category)

    db = client['github']
    collection = db[repos[1]["name"]]
    collection.insert_one({"name": repos[1]["name"], 
                            "readme": readme, 
                            "ProjectCompleteStatus": ProjectCompleteStatus, 
                            "MultiProjects": MultiProjects, 
                            "subProject": subProject, 
                            "category": category})


if __name__ == "__main__":
    # github_id = get_github_id()
    crawling("Tyranno-Rex")
    