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

# collection = db['repos-git-api-info']

# for repo in response.json():
#     data = {
#         'name': repo['name'],
#         'full_name': repo['full_name'],
#         'private': repo['private'],
#         'owner': repo['owner']['login'],
#         'html_url': repo['html_url'],
#         'description': repo['description'],
#         'url': repo['url'],
#         'languages_url': repo['languages_url'],
#         'contributors_url': repo['contributors_url'],
#         'created_at': repo['created_at'],
#         'updated_at': repo['updated_at'],
#         'pushed_at': repo['pushed_at'],
#         'size': repo['size'],
#         'stargazers_count': repo['stargazers_count'],
#         'visibility': repo['visibility']
#     }
#     collection.insert_one(data)


coord = {
    "graphic": [10, 5, 0],
    "ai": [10, -5, 10],
    "web/mobile": [5, 0, 5],
    "algorithm": [5, 0, 0],
    "os": [15, 5, 5],
    "network": [5, 5, 5],
    "game&simulation": [0, 5, 0],
    "security": [10, 0, 5],
    "optimization": [0, -5, 0],
    "implement": [5, 15, 5],
    "database": [0, -5, 10],
    "devops&publish": [0, 5, 10],
    "frontend": [10, -5, 0],
    "backend": [10, 5, 10],
    "fullstack": [0, 0, 5],
    "cloud": [5, 15, 15],
    "teamTask": [5, 10, 5],
    "other": [5, 5, 15]
}

/** 
* Paste one or more documents here
*/
{
  "distance": 168.29744,
  "optimal_coords": {
    "graphic": [
      10,
      5,
      0
    ],
    "ai": [
      10,
      -5,
      10
    ],
    "web/mobile": [
      5,
      0,
      5
    ],
    "algorithm": [
      5,
      0,
      0
    ],
    "os": [
      15,
      5,
      5
    ],
    "network": [
      5,
      5,
      5
    ],
    "game&simulation": [
      0,
      5,
      0
    ],
    "security": [
      10,
      0,
      5
    ],
    "optimization": [
      0,
      -5,
      0
    ],
    "implement": [
      5,
      15,
      5
    ],
    "database": [
      0,
      -5,
      10
    ],
    "devops&publish": [
      0,
      5,
      10
    ],
    "frontend": [
      10,
      -5,
      0
    ],
    "backend": [
      10,
      5,
      10
    ],
    "fullstack": [
      0,
      0,
      5
    ],
    "cloud": [
      5,
      15,
      15
    ],
    "teamTask": [
      5,
      10,
      5
    ],
    "other": [
      5,
      5,
      15
    ]
  }
}