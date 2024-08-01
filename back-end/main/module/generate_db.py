import numpy as np
from scipy.optimize import minimize
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import platform

# category weights
category_weight = [3, 2, 2, 2, 2]

# coordinates of each category
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

# get_weights is a function that returns a dictionary of category weights by combining the category and weight lists.
# return : dictionary of category weights
def get_weights(categories, weights):
    weight_dict = {category: weight for category, weight in zip(categories, weights)}
    return weight_dict

# weighted_distance is a function that calculates the weighted distance between the repository position and the category position.
# np.linalg.norm : calculates the Euclidean distance between two points
# return : weighted distance
def weighted_distance(repo_pos, categories, weights):
    distance = 0
    for category in categories:
        weight = weights.get(category, 1)  # 기본 가중치를 1로 설정
        category_pos = category_coords[category]
        distance += weight * np.linalg.norm(repo_pos - category_pos)
    return distance

# find_optimal_location is a function that finds the optimal location of the repository by minimizing the weighted distance.
# minimize : finds the minimum value of a function using the L-BFGS-B method
# L-BFGS-B : a limited-memory quasi-Newton optimization algorithm that approximates the Broyden-Fletcher-Goldfarb-Shanno (BFGS) algorithm
# return : optimal location
def find_optimal_location(categories, weights):
    initial_guess = np.zeros(3)
    result = minimize(weighted_distance, initial_guess, args=(categories, weights), method='L-BFGS-B')
    return result.x


# generate_database is a function that generates a database with the calculated repository and category positions.
# repo-position : that contains the repository name and its position
# category-positions : that contains the category name and its position
# repo-category : that contains the repository name and its categories
# return : none
def generate_database(client):
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

    collection.drop()
    # 레포지토리 위치 저장
    for repo, position in repo_optimal_locations.items():
        collection.insert_one({'repo': repo, 'position': position.tolist()})

    collection2.drop()
    # 카테고리 위치 저장
    for category, coord in category_coords.items():
        collection2.insert_one({'category': category, 'position': coord.tolist()})
    
    collection3.drop()
    # 레포지토리-카테고리 연결 저장
    for repo, categories in get_category_weights.items():
        # array 로 들어가게 수정
        categories = list(categories.keys())
        collection3.insert_one({'repo': repo, 'categories': categories})