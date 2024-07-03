import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 카테고리 중심 좌표 설정
category_coords = {
    'graphic': np.array([0, 0, 0]),
    'ai': np.array([10, 0, 0]),
    'web/mobile': np.array([0, 10, 0]),
    'algorithm': np.array([0, 0, 10]),
    'os': np.array([10, 10, 0]),
    'network': np.array([10, 0, 10]),
    'game&simulation': np.array([0, 10, 10]),
    'security': np.array([10, 10, 10]),
    'optimization': np.array([5, 5, 15]),
    'implement': np.array([15, 5, 5]),
    'database': np.array([5, 15, 5]),
    'devops&publish': np.array([5, 5, 5]),
    'other': np.array([5, 15, 15]),
}

# 레포지토리 데이터
repos = {
    'portfolio-project': ['graphic', 'ai', 'web/mobile', 'algorithm'],
    'algorithm': ['algorithm'],
    '42seoul-course': {
        'libft': ['implement'],
        'ft_printf': ['implement'],
        'get_next_line': ['implement'],
        'born2beRoot': ['os', 'implement', 'security', 'network'],
        'minitalk': ['network', 'implement'],
        'so_long': ['game&simulation', 'implement'],
        'push_swap': ['algorithm'],
        'minishell': ['implement', 'os'],
        'philosopher': ['os', 'implement', 'optimization'],
        'netpractice': ['network'],
        'cpp module 04': ['implement'],
        'cub3d': ['graphic', 'game&simulation'],
        'cpp module 09': ['implement'],
    },
    'fss_project': ['web/mobile', 'security', 'network', 'devops&publish'],
    'java-board-web': ['web/mobile', 'security'],
    'BE-study': {
        'study-database': ['database'],
        'study-os': ['os'],
        'study-server': ['ai', 'network'],
    },
    'FE-study': ['web/mobile'],
    'minishell': ['implement'],
    'profpilot': ['web/mobile', 'security', 'network', 'devops&publish'],
    'ft_irc': ['network'],
    'gvdb-fluid-unreal': ['game&simulation', 'optimization', 'algorithm'],
    'cub3d': ['graphic', 'game&simulation'],
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
        'Game_Engineering': ['game&simulation', 'optimization', 'algorithm'],
        'Game_Graphics_Programming': ['graphic'],
        'OpenSource_SW_Development_Methods_and_Tools': ['os', 'other'],
        'Operating_System': ['os'],
    },
    'kyunghee 2-2': {
        'game engine basic': ['game&simulation'],
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

# 가중 평균 계산 함수
def weighted_average(coords, weights):
    return np.average(coords, axis=0, weights=weights)

# 레포지토리 위치 계산
repo_positions = {}

for repo, categories in repos.items():
    if isinstance(categories, dict):
        for sub_repo, sub_categories in categories.items():
            category_coords_list = [category_coords[cat] for cat in sub_categories]
            weights = [len(sub_categories) - i for i in range(len(sub_categories))]
            repo_positions[f'{repo}/{sub_repo}'] = weighted_average(category_coords_list, weights)
    else:
        category_coords_list = [category_coords[cat] for cat in categories]
        weights = [len(categories) - i for i in range(len(categories))]
        repo_positions[repo] = weighted_average(category_coords_list, weights)

# print(repo_positions)
# print(category_coords)


# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure

# client = MongoClient('localhost', 27017)

# try:
#     # 연결 테스트
#     client.admin.command('ismaster')
#     print('MongoDB connection successful.')
# except ConnectionFailure:
#     print('MongoDB server not available.')

# db = client['portfolio']
# collection = db['category']
# collection2 = db['repo']

# for repo, position in repo_positions.items():
#     # print(repo, position)
#     collection2.insert_one({'repo': repo
#                             , 'position': position.tolist()})
# for category, coord in category_coords.items():
#     # print(category, coord)
#     collection.insert_one({'category': category
#                             , 'coord': coord.tolist()})




# 3D 시각화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 카테고리 중심 플롯
for category, coord in category_coords.items():
    ax.scatter(*coord, label=category, s=100)

# 레포지토리 위치 플롯
for repo, position in repo_positions.items():
    ax.scatter(*position, label=repo, s=50)

ax.legend()
plt.show()
