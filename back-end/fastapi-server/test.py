from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient('localhost', 27017)

db = client['portfolio']
collection2 = db['all_distance']

# 모든 정보를 가져와서 평균 distance를 구한다.
all_distance = collection2.find()
sum = 0
count = 0
for distance in all_distance:
    sum += distance['distance']
    count += 1

average_distance = sum / count
print(average_distance)