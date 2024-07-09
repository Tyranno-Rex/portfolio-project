import numpy as np
import random
from scipy.optimize import minimize
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


# 다양한 시도를 통해서 해당 위치에 해당 카테고리를 배치했을 때 지금까지는 최적의 위치라고 판단이 되었다.
# 때문에 이제는 이 최적의 위치를 저장하고, 이를 통해서 레포지토리들의 위치를 계산할 수 있도록 한다.
# {
#   "database": [5, 14, 0],
#   "os": [2, 10, 0],
#   "security": [5, -8, 5],
#   "teamTask": [2, 4, 5]
# }


# {
#     ai[5, -2, 0]
#     algorithm [2.  -6, 0]
# }

coords_data = [
    # np.array([5, -2, 0]),
    # np.array([2, -6, 0]),
    np.array([5, -10, 0]),
    np.array([2, -14, 0]),
    np.array([2, 2, 0]),
    np.array([5, 6, 0]),
    np.array([2, 10, 0]),
    # np.array([5, 14, 0]),
    np.array([5, 0, 5]),
    np.array([2, -4, 5]),
    np.array([5, -8, 5]),
    np.array([2, 4, 5]),
    np.array([5, 8, 5]),
    np.array([2, 0, -5]),
    np.array([5, -4, -5]),
    np.array([2, -8, -5]),
    np.array([5, 4, -5]),
    np.array([2, 8, -5]),
]

categories_data = [
    'graphic',
    # 'ai',
    'web/mobile',
    # 'algorithm',
    'os',
    'network',
    'game&simulation',
    'security',
    'optimization',
    'implement',
    # 'database',
    'devops&publish',
    'frontend',
    'backend',
    'fullstack',
    'cloud',
    'teamTask',
    'other',
]


# 레포지토리 데이터
repos = {
    'portfolio-project': ['graphic', 'ai', 'web/mobile', 'algorithm', 'fullstack'],
    'algorithm': ['algorithm'],
    '42seoul-course': {
        'libft': ['implement'],
        'ft_printf': ['implement'],
        'get_next_line': ['implement'],
        'born2beRoot': ['os', 'implement', 'security', 'network'],
        'minitalk': ['network', 'implement'],
        'so_long': ['game&simulation', 'implement'],
        'push_swap': ['algorithm', 'implement', 'optimization'],
        'minishell': ['implement', 'os', 'teamTask'],
        'philosopher': ['os', 'implement', 'optimization'],
        'netpractice': ['network'],
        'cpp module 04': ['implement'],
        'cub3d': ['graphic', 'game&simulation', 'algorithm', 'teamTask'],
        'cpp module 09': ['implement'],
        'ft_irc': ['network', 'implement', 'teamTask'],
    },
    'fss_project': ['web/mobile', 'security', 'network', 'devops&publish', 'fullstack'],
    'java-board-web': ['web/mobile', 'security', 'fullstack'],
    'BE-study': {
        'study-database': ['database'],
        'study-os': ['os'],
        'study-server': ['ai', 'network', 'backend', 'implement', 'cloud'],
    },
    'FE-study': ['frontend', 'web/mobile'],
    'profpilot': ['web/mobile', 'security', 'network', 'devops&publish'],
    'gvdb-fluid-unreal': ['game&simulation', 'optimization', 'algorithm', 'teamTask', 'graphic'],
    'webtoonProject': ['web/mobile'],
    'kyunghee 3-2': {
        'Algorithm': ['algorithm'],
        'ComputerNetwork': ['network'],
        'Database': ['database'],
        'FullStackServiceProgramming': ['web/mobile', 'security', 'network', 'devops&publish'],
        'LatestTechnologyColloquium2': ['other'],
        'OOP': ['implement'],
        'softwareEngineering': ['other'],
    },
    'kyunghee 3-1': {
        '3D data processing': ['algorithm', 'graphic'],
        'AI_and_Game_Programming': ['ai', 'algorithm'],
        'Game_Engineering': ['game&simulation', 'optimization', 'algorithm', 'teamTask', 'graphic'],
        'Game_Graphics_Programming': ['graphic'],
        'OpenSource_SW_Development_Methods_and_Tools': ['os', 'other'],
        'Operating_System': ['os'],
    },
    'kyunghee 2-2': {
        'game engine basic': ['game&simulation', 'teamTask'],
        'game programming introduction': ['algorithm', 'implement'],
        'Introduction to software convergence': ['algorithm'],
        'data structure': ['algorithm'],
    },
    '42 piscine': {
        'C': ['implement', 'algorithm'],
        'Rush': ['algorithm', 'implement'],
        'Shell': ['os'],
    },
}


import sys

distance_total = sys.maxsize
optimal_locations = {}
optimal_coords = {}

category_len1 = [1]
category_len2 = [1, 1]
category_len3 = [1, 1, 1]
category_len4 = [1, 1, 1, 1]
category_len5 = [1, 1, 1, 1, 1]

def get_weights(categories, weights):
    weight_dict = {category: weight for category, weight in zip(categories, weights)}
    print(weight_dict)
    return weight_dict


category_weights = {
    'portfolio-project': get_weights(repos['portfolio-project'], category_len5),
    'algorithm': get_weights(repos['algorithm'], category_len1),
    'libft': get_weights(repos['42seoul-course']['libft'], category_len1),
    'ft_printf': get_weights(repos['42seoul-course']['ft_printf'], category_len1),
    'get_next_line': get_weights(repos['42seoul-course']['get_next_line'], category_len1),
    'born2beRoot': get_weights(repos['42seoul-course']['born2beRoot'], category_len4),
    'minitalk': get_weights(repos['42seoul-course']['minitalk'], category_len2),
    'so_long': get_weights(repos['42seoul-course']['so_long'], category_len2),
    'push_swap': get_weights(repos['42seoul-course']['push_swap'], category_len4),
    'minishell': get_weights(repos['42seoul-course']['minishell'], category_len4),
    'philosopher': get_weights(repos['42seoul-course']['philosopher'], category_len4),
    'netpractice': get_weights(repos['42seoul-course']['netpractice'], category_len1),
    'cpp module 04': get_weights(repos['42seoul-course']['cpp module 04'], category_len1),
    'cub3d': get_weights(repos['42seoul-course']['cub3d'], category_len4),
    'cpp module 09': get_weights(repos['42seoul-course']['cpp module 09'], category_len1),
    'ft_irc': get_weights(repos['42seoul-course']['ft_irc'], category_len4),
    'fss_project': get_weights(repos['fss_project'], category_len5),
    'java-board-web': get_weights(repos['java-board-web'], category_len5),
    'study-database': get_weights(repos['BE-study']['study-database'], category_len1),
    'study-os': get_weights(repos['BE-study']['study-os'], category_len1),
    'study-server': get_weights(repos['BE-study']['study-server'], category_len5),
    'FE-study': get_weights(repos['FE-study'], category_len5),
    'profpilot': get_weights(repos['profpilot'], category_len5),
    'gvdb-fluid-unreal': get_weights(repos['gvdb-fluid-unreal'], category_len5),
    'webtoonProject': get_weights(repos['webtoonProject'], category_len5),
    'Algorithm': get_weights(repos['kyunghee 3-2']['Algorithm'], category_len1),
    'ComputerNetwork': get_weights(repos['kyunghee 3-2']['ComputerNetwork'], category_len1),
    'Database': get_weights(repos['kyunghee 3-2']['Database'], category_len1),
    'FullStackServiceProgramming': get_weights(repos['kyunghee 3-2']['FullStackServiceProgramming'], category_len5),
    'LatestTechnologyColloquium2': get_weights(repos['kyunghee 3-2']['LatestTechnologyColloquium2'], category_len5),
    'OOP': get_weights(repos['kyunghee 3-2']['OOP'], category_len1),
    'softwareEngineering': get_weights(repos['kyunghee 3-2']['softwareEngineering'], category_len5),
    '3D data processing': get_weights(repos['kyunghee 3-1']['3D data processing'], category_len2),
    'AI_and_Game_Programming': get_weights(repos['kyunghee 3-1']['AI_and_Game_Programming'], category_len2),
    'Game_Engineering': get_weights(repos['kyunghee 3-1']['Game_Engineering'], category_len5),
    'Game_Graphics_Programming': get_weights(repos['kyunghee 3-1']['Game_Graphics_Programming'], category_len1),
    'OpenSource_SW_Development_Methods_and_Tools': get_weights(repos['kyunghee 3-1']['OpenSource_SW_Development_Methods_and_Tools'], category_len2),
    'Operating_System': get_weights(repos['kyunghee 3-1']['Operating_System'], category_len1),
    'game engine basic': get_weights(repos['kyunghee 2-2']['game engine basic'], category_len2),
    'game programming introduction': get_weights(repos['kyunghee 2-2']['game programming introduction'], category_len2),
    'Introduction to software convergence': get_weights(repos['kyunghee 2-2']['Introduction to software convergence'], category_len2),
    'data structure': get_weights(repos['kyunghee 2-2']['data structure'], category_len2),
    'C': get_weights(repos['42 piscine']['C'], category_len2),
    'Rush': get_weights(repos['42 piscine']['Rush'], category_len2),
    'Shell': get_weights(repos['42 piscine']['Shell'], category_len1),
}

# 거리 계산 함수
def weighted_distance(repo_pos, categories, weights, new_coords):
    try :
        distance = 0
        for category in categories:
            weight = weights.get(category, 1)  # 기본 가중치를 1로 설정
            category_pos = new_coords[category]
            distance += weight * np.linalg.norm(repo_pos - category_pos)
        return distance
    except KeyError:
        print(f'KeyError: {categories}')
        exit()

# 최적의 위치 계산 함수
def find_optimal_location(categories, weights, coords):
    initial_guess = np.zeros(3)
    result = minimize(weighted_distance, initial_guess, args=(categories, weights, coords), method='L-BFGS-B')
    distance = weighted_distance(result.x, categories, weights, coords)
    # print(f'{categories} 최적의 위치: {result.x}, 거리: {distance}')
    return result.x, distance

def make_new_category_coords():
    new_category_coords = {}
    cp_coords = coords_data.copy()
    random.shuffle(cp_coords)
    for category in categories_data:
        new_category_coords[category] = cp_coords.pop()
    new_category_coords["database"] = np.array([5, 14, 0])
    new_category_coords["ai"] = np.array([5, -2, 0])
    new_category_coords["algorithm"] = np.array([2, -6, 0])
    return new_category_coords

client = MongoClient('localhost', 27017)

try:
    # 연결 테스트
    client.admin.command('ismaster')
    db = client['github']
    print('Connected to MongoDB')
except ConnectionFailure:
    print('MongoDB server not available')

db = client['portfolio']
collection = db['find_category_minimal_pos']
# collection2 = db['all_distance']

# mongodb에서 가장 최근의 데이터를 가져옴
try:
    recent_data = collection.find().sort('_id', -1).limit(1)[0]
    distance_total = recent_data['distance']
    optimal_coords = {key: np.array(value) for key, value in recent_data['optimal_coords'].items()}
    print(f'가장 최근의 데이터로 초기화: {distance_total}')
except IndexError:
    print('최근의 데이터가 없습니다.')


i = 0
while True:
    repo_optimal_locations = {}
    distance_try = 0

    new_category_coords = make_new_category_coords()
    # 레포지토리 별 최적의 위치 계산
    for repo, categories in repos.items():
        if isinstance(categories, dict):
            repo_optimal_locations[repo] = {}
            for sub_repo, sub_categories in categories.items():
                weights = category_weights[sub_repo]
                optimal_location, distance = find_optimal_location(sub_categories, weights, new_category_coords)
                repo_optimal_locations[repo][sub_repo] = optimal_location
        else:
            weights = category_weights[repo]
            optimal_location, distance = find_optimal_location(categories, weights, new_category_coords)
            repo_optimal_locations[repo] = optimal_location
        distance_try += distance
    
    if distance_try < distance_total:
        distance_total = round(distance_try, 5)
        optimal_locations = repo_optimal_locations
        optimal_coords = new_category_coords
        # bson.errors.InvalidDocument: cannot encode object: array([7.20688665, 0.8878323 , 5.32456981]), of type: <class 'numpy.ndarray'>
        collection.insert_one({
            'distance': distance_total,
            'optimal_coords': {key: value.tolist() for key, value in optimal_coords.items()}
        })
    # else :
    #     collection2.insert_one({
    #         'distance' : distance_try
    #     })
        
    
    print(f'{i+1}번째 시도: {distance_try}')
    i += 1