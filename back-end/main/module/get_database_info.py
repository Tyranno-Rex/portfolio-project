

# Find the data for a repository in the database using the repository name
# Return : Dictionary containing the name, url, readme, description, complete_status, multi, category, and subproject of the repository
def find_repo_data(repo_name, client):
    try:
        # Use a context manager to ensure the MongoClient is closed properly
        db = client['portfolio']
        repos = db['database']

        # If '/' exists in repo_name, set repo_name to the part after '/'
        if '/' in repo_name:
            repo_name = repo_name.split('/')[1]

        repo = repos.find_one({"name": repo_name})
        if repo is None:
            raise ValueError(f"Repository {repo_name} not found in the database")

        response = {
            "name": repo.get('name', 'default_name'),
            "url": repo.get('url', 'default_url'),
            "readme": repo.get('readme', 'default_readme'),
            "description": repo.get('description', 'default_description'),
            "complete_status": repo.get('complete_status', 'default_status'),
            "multi": repo.get('multi', 'default_multi'),
            "category": repo.get('category', 'default_category'),
            "subproject": repo.get('subproject', 'default_subproject')
        }

    except Exception as e:
        # Handle exceptions and ensure resources are freed
        print(f"Error finding repository data: {e}")
        raise e

    return response

