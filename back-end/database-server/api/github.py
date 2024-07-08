from requests import get
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# client = MongoClient('localhost', 27017)

OWNER_NAE = "Tyranno-Rex"
# try:
#     # 연결 테스트
#     client.admin.command('ismaster')
#     db = client['github']
#     print('Connected to MongoDB')
# except ConnectionFailure:
#     print('MongoDB server not available')

# 1. 모든 repository의 이름과 url을 가져온다.
token = open("C:/Users/admin/project/back/back-end/database-server/api/database/git-token.txt", "r").read().strip()

url_all_repos = "https://api.github.com/user/repos"
headers_all_repos = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"
}

response_all_repos = get(url_all_repos, headers=headers_all_repos)
json_all_repos = response_all_repos.json()
repo_all_list = []

for json in json_all_repos:
    repo_all_list.append({
        "name": json["name"],
        "url": json["html_url"]
    })

# 2. 각 repository의 README.md를 가져온다.
import base64

def decode_base64(content):
    base64_bytes = content.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')

for repo in repo_all_list:
    if repo["name"] not in ["BE-study", "portfolio-project"]:
        continue
    
    url_readme = f"https://api.github.com/repos/{OWNER_NAE}/{repo['name']}/readme"
    headers_readme = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response_readme = get(url_readme, headers=headers_readme)

    if response_readme.status_code == 200:
        json_readme = response_readme.json()
        encoded_content = json_readme["content"]
        decoded_content = decode_base64(encoded_content)
        repo["readme"] = decoded_content
        project_name = decoded_content.split('PROJECT_NAME : ')[1].split('\n')[0],
        project_description = decoded_content.split('PROJECT_DESCRIPTION : ')[1].split('\n')[0],
        project_url = decoded_content.split('PROJECT_URL : ')[1].split('\n')[0],
        project_complete_status = decoded_content.split('PROJECT_COMPLETION_STATUS : ')[1].split('\n')[0],
        project_multi = decoded_content.split('PROJECT_MULTI : ')[1].split('\n')[0],
        project_category = decoded_content.split('PROJECT_CATEGORY : ')[1].split('\n')[0],
        project_subproject = decoded_content.split('PROJECT_SUBPROJECT : ')[1].split('\n')[0]


        repo['description'] = project_description
        repo['complete_status'] = project_complete_status
        repo['multi'] = project_multi
        project_category = project_category[0].split(', ')
        repo['category'] = project_category
        project_subproject = project_subproject.split(', ')
        repo['subproject'] = project_subproject
    
        multi = project_multi[0]
        
        # 3. 각 repository에서 세부 파일에서 readme가 있는 경우 가져온다.
        if multi == 'TRUE':
            for sub_project in project_subproject:
                url_sub_readme = f"https://api.github.com/repos/{OWNER_NAE}/{repo['name']}/contents/{sub_project}"
                headers_sub_readme = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {token}",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                response_sub_readme = get(url_sub_readme, headers=headers_sub_readme)
                json_sub_readme = response_sub_readme.json()
                for json in json_sub_readme:
                    if (json["name"] == "README.md"):
                        url_sub_readme = json["download_url"]
                        response_sub_readme = get(url_sub_readme)
                        decoded_content = response_sub_readme.text
                        sub_project_name = decoded_content.split('PROJECT_NAME : ')[1].split('\n')[0]
                        sub_project_description = decoded_content.split('PROJECT_DESCRIPTION : ')[1].split('\n')[0]
                        sub_project_url = decoded_content.split('PROJECT_URL : ')[1].split('\n')[0]
                        sub_project_complete_status = decoded_content.split('PROJECT_COMPLETION_STATUS : ')[1].split('\n')[0]
                        sub_project_multi = decoded_content.split('PROJECT_MULTI : ')[1].split('\n')[0]
                        sub_project_category = decoded_content.split('PROJECT_CATEGORY : ')[1].split('\n')[0]
                        sub_project_subproject = decoded_content.split('PROJECT_SUBPROJECT : ')[1].split('\n')[0]
                        repo_all_list.append({
                            "name": sub_project_name,
                            "url": sub_project_url,
                            "readme": decoded_content,
                            "description": sub_project_description,
                            "complete_status": sub_project_complete_status,
                            "multi": sub_project_multi,
                            "category": sub_project_category,
                            "subproject": sub_project_subproject
                        })
    else:
        repo["readme"] = ""


for repo in repo_all_list:
    if (repo["name"] != "BE-study" and repo["name"] != "portfolio-project" 
        and repo["name"] != "study-os" and repo["name"] != "study-server" and repo["name"] != "study-database"):
        continue
    print(repo["name"])
    print(repo["url"])
    # print(repo["readme"])
    print(repo["description"])
    print(repo["complete_status"])
    print(repo["multi"])
    print(repo["category"])
    print(repo["subproject"])
    print("")



