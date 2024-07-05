from requests import get
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient('localhost', 27017)

try:
    # 연결 테스트
    client.admin.command('ismaster')
    db = client['github']
    print('Connected to MongoDB')
except ConnectionFailure:
    print('MongoDB server not available')

token = open("./back-end/database-server/api/database/git-token.txt", "r").read().strip()
url = "https://api.github.com/user/repos"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"
}

response = get(url, headers=headers)
json = response.json()

i = 0 
for repo in json:
    if (i == 3):
        print(repo)
    i += 1