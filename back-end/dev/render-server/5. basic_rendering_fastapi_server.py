from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware


class FASTAPI_SERVER:
    def __init__(self):

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.router = APIRouter()
        self.router.add_api_route('/', endpoint=self.root)
        self.router.add_api_route('/repos', endpoint=self.get_all_repos, methods=['GET'])
        self.router.add_api_route('/categories', endpoint=self.get_all_categories, methods=['GET'])
        self.app.include_router(self.router)
        self.repos, self.categories = self.get_db()

    async def root(self):
        return {"message": "Hello World"}

    def get_db(self):
        client = MongoClient('localhost', 27017)
        db = client['portfolio']
        repos = db['repo-positions']
        categories = db['category-positions']
        return repos, categories
    
    def get_all_repos(self):
        repos = self.repos.find()
        json_repos = []
        for repo in repos:
            json_repos.append({'repo': repo['repo'], 'position': repo['position']})
        return json_repos
    
    def get_all_categories(self):
        categories = self.categories.find()
        json_categories = []
        for category in categories:
            json_categories.append({'category': category['category'], 'position': category['position']})
        return json_categories

if __name__ == "__main__":
    server = FASTAPI_SERVER()
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8000)

