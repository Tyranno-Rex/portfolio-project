
from pymongo import MongoClient

PASSWORD = open("C:/Users/admin/project/portfolio-project/back-end/main/database/mongodb.txt", "r").read().strip()
MONGO_CNN = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")


db = MONGO_CNN.hobby

doc = {'name':'bobby','age':21}
db.test.insert_one(doc)