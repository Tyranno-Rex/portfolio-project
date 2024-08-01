from bson import ObjectId
from pymongo import MongoClient
import platform

# Save the repo data in the MongoDB
# Compare the data with the existing data in the MongoDB
# If the data is not inserted, insert the data
# Insert    : no existing data, 
# Update    : existing data is different from the new data
# Skip      : existing data is same as the new data
# return    : True if the data is inserted, False if the data is not inserted
def save_repo_data_in_mongo(repo, client):    
    db = client['portfolio']
    repos = db['database']

    past_repo = repos.find_one({"name": repo["name"]})
    
    if past_repo is None:
        print("Insert: ", repo["name"])
        repo['_id'] = str(ObjectId())
        repos.insert_one(repo)
        client.close()
        return True
    
    past_name = past_repo["name"][0]
    repo_name = repo["name"][0]
    past_url = past_repo["url"][0]
    repo_url = repo["url"][0]
    past_readme = past_repo["readme"]
    repo_readme = repo["readme"]
    repo_description = repo["description"][0]
    past_description = past_repo["description"][0]
    repo_complete_status = repo["complete_status"][0]
    past_complete_status = past_repo["complete_status"][0]
    repo_multi = repo["multi"][0]
    past_multi = past_repo["multi"][0]
    repo_category = repo["category"][0]
    past_category = past_repo["category"][0]
    repo_subproject = repo["subproject"][0]
    past_subproject = past_repo["subproject"][0]

    if past_repo is not None and\
            past_name == repo_name and\
            past_url == repo_url and\
            past_readme == repo_readme and\
            past_description == repo_description and\
            past_complete_status == repo_complete_status and\
            past_multi == repo_multi and\
            past_category == repo_category and\
            past_subproject == repo_subproject:
        print("Skip: ", repo["name"])
    else:
        print("Update: ", repo["name"])
        repos.update_one({"name": repo["name"]}, {"$set": repo})
    
    client.close()

