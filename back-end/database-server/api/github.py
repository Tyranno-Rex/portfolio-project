from requests import get

token = open("./back-end/database-server/api/database/git-token.txt", "r").read().strip()
url = "https://api.github.com/user/repos"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + token,
    "X-GitHub-Api-Version": "2022-11-28"
}

response = get(url, headers=headers)

for repo in response.json():
    print("=====================================")
    print(repo['name'], repo['full_name'], repo['private'], repo['owner']['login'], repo['html_url'], repo['description'], repo['url'], repo['languages_url'], repo['contributors_url'], repo['created_at'], repo['updated_at'], repo['pushed_at'], repo['size'], repo['stargazers_count'], repo['visibility'])
