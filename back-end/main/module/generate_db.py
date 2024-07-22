import numpy as np
from scipy.optimize import minimize
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import platform

category_weight = [3, 2, 2, 2, 2]

# 카테고리 좌표
category_coords = {
    'game&simulation':  np.array([-3, -5, -8]),
    'optimization':     np.array([3, -5, -4]),
    'graphic':          np.array([-3, -5, 0]),
    'security':         np.array([3, -5, 4]),
    'fullstack':        np.array([-3, -5, 8]),
    
    'os':               np.array([-3, 0, -14]),
    'teamTask':         np.array([3, 0, -10]),
    'algorithm':        np.array([-3, 0, -6]),
    'ai':               np.array([3, 0, -2]),
    'devops&publish':   np.array([-3, 0, 2]),
    'web/mobile':       np.array([3, 0, 6]),
    'other':            np.array([-3, 0, 10]),
    'database':         np.array([3, 0, 14]),

    'implement':        np.array([3, 5, -8]),
    'backend':          np.array([-3, 5, -4]),
    'cloud':            np.array([3, 5, 0]),
    'network':          np.array([-3, 5, 4]),
    'frontend':         np.array([3, 5, 8]),
}


def get_weights(categories, weights):
    weight_dict = {category: weight for category, weight in zip(categories, weights)}
    return weight_dict

# 거리 계산 함수
def weighted_distance(repo_pos, categories, weights):
    distance = 0
    for category in categories:
        weight = weights.get(category, 1)  # 기본 가중치를 1로 설정
        category_pos = category_coords[category]
        distance += weight * np.linalg.norm(repo_pos - category_pos)

    return distance

# 최적의 위치 계산 함수
def find_optimal_location(categories, weights):
    initial_guess = np.zeros(3)
    result = minimize(weighted_distance, initial_guess, args=(categories, weights), method='L-BFGS-B')
    return result.x

def generate_database():
    current_os = platform.system()
    if current_os == 'Windows':
        PASSWORD = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-mongo-token.txt", "r").read().strip()
    else:
        PASSWORD = open("/app/mongo-token.txt", "r").read().strip()
    client = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")
    try:
        # 연결 테스트
        client.admin.command('ismaster')
        print('Connected to MongoDB')
    except ConnectionFailure:
        print('MongoDB server not available')

    # 데이터베이스, 컬렉션 로드
    db = client['portfolio']
    database = db['database']
    collection  = db['repo-positions']
    collection2 = db['category-positions']
    collection3 = db['repo-category']

    # 레포지토리 별 카테고리 가중치 계산
    get_category_weights = {}
    for db in database.find():
        category_list = db['category'].split(', ')
        for i in range(len(category_list)):
            category_list[i] = category_list[i].replace("'", "")
        get_category_weights[db['name']] = get_weights(category_list, category_weight)

    # 레포지토리 별 최적의 위치 계산
    repo_optimal_locations = {}
    for repo, categories in get_category_weights.items():
        weights = get_category_weights[repo]
        if 'NONE' in categories:
            continue
        optimal_location = find_optimal_location(categories, weights)
        repo_optimal_locations[repo] = optimal_location

    # 레포지토리 위치 저장
    for repo, position in repo_optimal_locations.items():
        collection.insert_one({'repo': repo, 'position': position.tolist()})

    for category, coord in category_coords.items():
        collection2.insert_one({'category': category, 'position': coord.tolist()})
    
    for repo, categories in get_category_weights.items():
        # array 로 들어가게 수정
        categories = list(categories.keys())
        collection3.insert_one({'repo': repo, 'categories': categories})
    client.close()