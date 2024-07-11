import numpy as np
from scipy.optimize import minimize
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


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


# 레포지토리 데이터
repos = {
    'portfolio-project': ['graphic', 'ai', 'web/mobile', 'algorithm', 'fullstack'],
    'algorithm': ['algorithm'],
    '42seoul-course': {
        'libft': ['implement'],
        'ft_printf': ['implement'],
        'get_next_line': ['implement'],
        'Born2BeRoot': ['os', 'implement', 'security', 'network'],
        'exam-rank02' : ['implement'],
        'minitalk': ['network', 'implement'],
        'so_long': ['game&simulation', 'implement'],
        'push_swap': ['algorithm', 'implement', 'optimization'],
        'exam-rank03': ['implement'],
        'minishell': ['implement', 'os', 'teamTask'],
        'philosopher': ['os', 'implement', 'optimization'],
        'exam-rank04': ['implement'],
        'netpractice': ['network'],
        'CPPModule04': ['implement'],
        'cub3d': ['graphic', 'game&simulation', 'algorithm', 'teamTask'],
        'CPPModule09': ['implement'],
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


category_len1 = [3]
category_len2 = [3, 2]
category_len3 = [3, 2, 2]
category_len4 = [3, 2, 2, 2]
category_len5 = [3, 2, 2, 2, 2]

def get_weights(categories, weights):
    weight_dict = {category: weight for category, weight in zip(categories, weights)}
    return weight_dict

category_weights = {
    'portfolio-project': get_weights(repos['portfolio-project'], category_len5),
    'algorithm': get_weights(repos['algorithm'], category_len1),
    'libft': get_weights(repos['42seoul-course']['libft'], category_len1),
    'ft_printf': get_weights(repos['42seoul-course']['ft_printf'], category_len1),
    'get_next_line': get_weights(repos['42seoul-course']['get_next_line'], category_len1),
    'Born2BeRoot': get_weights(repos['42seoul-course']['Born2BeRoot'], category_len4),
    'minitalk': get_weights(repos['42seoul-course']['minitalk'], category_len2),
    'so_long': get_weights(repos['42seoul-course']['so_long'], category_len2),
    'push_swap': get_weights(repos['42seoul-course']['push_swap'], category_len4),
    'minishell': get_weights(repos['42seoul-course']['minishell'], category_len4),
    'philosopher': get_weights(repos['42seoul-course']['philosopher'], category_len4),
    'netpractice': get_weights(repos['42seoul-course']['netpractice'], category_len1),
    'CPPModule04': get_weights(repos['42seoul-course']['CPPModule04'], category_len1),
    'cub3d': get_weights(repos['42seoul-course']['cub3d'], category_len4),
    'CPPModule09': get_weights(repos['42seoul-course']['CPPModule09'], category_len1),
    'ft_irc': get_weights(repos['42seoul-course']['ft_irc'], category_len4),
    'exam-rank02': get_weights(repos['42seoul-course']['exam-rank02'], category_len1),
    'exam-rank03': get_weights(repos['42seoul-course']['exam-rank03'], category_len1),
    'exam-rank04': get_weights(repos['42seoul-course']['exam-rank04'], category_len1),
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

# 레포지토리 별 최적의 위치 계산
repo_optimal_locations = {}
for repo, categories in repos.items():
    if isinstance(categories, dict):
        repo_optimal_locations[repo] = {}
        for sub_repo, sub_categories in categories.items():
            weights = category_weights[sub_repo]
            optimal_location = find_optimal_location(sub_categories, weights)
            repo_optimal_locations[repo][sub_repo] = optimal_location
    else:
        weights = category_weights[repo]
        optimal_location = find_optimal_location(categories, weights)
        repo_optimal_locations[repo] = optimal_location

client = MongoClient('localhost', 27017)

try:
    # 연결 테스트
    client.admin.command('ismaster')
    db = client['github']
    print('Connected to MongoDB')
except ConnectionFailure:
    print('MongoDB server not available')

db = client['portfolio']
collection  = db['repo-positions']
collection2 = db['category-positions']
collection3 = db['repo-category']
col = db['repo-category']


# 레포지토리 위치 저장
for repo, position in repo_optimal_locations.items():
    if isinstance(position, dict):
        for sub_repo, sub_position in position.items():
            collection.insert_one({'repo': f'{repo}/{sub_repo}', 'position': sub_position.tolist()})
    else:
        collection.insert_one({'repo': repo, 'position': position.tolist()})

for category, coord in category_coords.items():
    collection2.insert_one({'category': category, 'position': coord.tolist()})
    

for repo, categories in repos.items():
    if isinstance(categories, dict):
        for sub_repo, sub_categories in categories.items():
            collection3.insert_one({'repo': f'{repo}/{sub_repo}', 'categories': sub_categories})
    else:
        collection3.insert_one({'repo': repo, 'categories': categories})
