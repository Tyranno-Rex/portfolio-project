# github의 닉네임을 받는다
def get_github_id():
    github_id = input("Github ID를 입력하세요: ")
    return github_id



# github의 닉네임을 받아서 해당 유저의 저장소를 크롤링한다
def crawling(github_id):
    import requests
    from bs4 import BeautifulSoup

    github_url = "github.com"
    github_personal_url = f"https://{github_url}/{github_id}?tab=repositories"
    response = requests.get(github_personal_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repos = []
    for i, repo in enumerate(soup.select("h3 > a")):
        repo_url = f"https://{github_url}{repo['href']}"
        repos.append({"name": repo.text.strip(), "url": repo_url})
    
    # 해당 주소의 모든 저장소의 세부 정보(readme, 주요 언어, commit 횟수, star 수, fork 수)를 크롤링한다
    
    # 1. 저장소의 readme를 크롤링한다
    # class="Link--primary"를 찾아서 readme를 크롤링한다
    response2 = requests.get(repos[0]["url"])
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    readme = soup2.find_all(class_="Link--primary")
    print(repos[0]["name"])
    for i, file in enumerate(readme):
        print(file.text)
    
    
    
    # first_file = soup(class_="Link--primary")
    # for i, file in enumerate(first_file):
    #     print(file.text)
    # print()
    
    
    # https://github.com/Tyranno-Rex/42seoul-course


if __name__ == "__main__":
    # github_id = get_github_id()
    crawling("Tyranno-Rex")
    