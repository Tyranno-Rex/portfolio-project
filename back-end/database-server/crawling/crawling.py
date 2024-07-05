import requests
from bs4 import BeautifulSoup

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




    response2 = requests.get(repos[0]["url"])
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    readme = soup2.select_one("article.markdown-body.entry-content.container-lg").text.strip()
    # print(readme)
# Project Category - for crawling
# PROJECT COMPLETION STATUS : TRUE
# MULIT PROJECTS : TRUE

# 'study-database': 'database'
# 'study-os': 'os'
# 'study-server': ['ai', 'network', 'backend', 'implement', 'cloud']

    # 해당 내용은 이제 DB에 저장해야 한다

    Project_Crawling_info = readme.split('Project Category - for crawling')[1].strip()
    print(Project_Crawling_info)
    ProjectCompleteStatus = Project_Crawling_info.split('PROJECT COMPLETION STATUS : ')[1].split('\n')[0]
    MultiProjects = Project_Crawling_info.split('MULIT PROJECTS : ')[1].split('\n')[0]
    
    print(ProjectCompleteStatus)
    print(MultiProjects)
    # if MultiProjects == 'TRUE':
    #     ProjectCategory = Project_Crawling_info.split('PROJECT CATEGORY : ')[1].split('\n')[0]
    #     print(ProjectCategory)
    # else:
    #     ProjectCategory = Project_Crawling_info.split('PROJECT CATEGORY : ')[1].split('\n')[0]
    #     print(ProjectCategory)

    
    # # 1. 저장소의 readme를 크롤링한다
    # response2 = requests.get(repos[0]["url"])
    # soup2 = BeautifulSoup(response2.text, 'html.parser')
    # readme = soup2.select_one("article.markdown-body.entry-content.container-lg").text.strip()
    # print(readme)

    
    # first_file = soup(class_="Link--primary")
    # for i, file in enumerate(first_file):
    #     print(file.text)
    # print()
    
    
    # https://github.com/Tyranno-Rex/42seoul-course


if __name__ == "__main__":
    # github_id = get_github_id()
    crawling("Tyranno-Rex")
    