import requests
import json

repos = []
headers = {'Authorization': 'token ' + 'd6ca43223530b01cb13a51af0dc62b354e9eb3a3'}
language = "Python"
filename = f"{language}_machine_learning.json"
# print(f"creating file: '{filename}'")
for number in range(1, 11):
    results = requests.get(
        f'https://api.github.com/search/repositories?q=machine_learning+language:python&per_page=100&page={number}',
        headers=headers).json()
    try:
        for repo in results['items']:
            repo_name = repo['full_name']
            repo_lang = repo['language']
            repo_created = repo['created_at']
            repo_updated = repo['updated_at']

            print(
                f"Repository {repo_name}"
                f"Repository {repo_lang}"
                f"Repository {repo_created}"
            )
            repos.append(
                {
                    "repo": repo_name,
                    "language": repo_lang,
                    "created_at": repo_created,
                    "updated_at": repo_updated
                }
            )
    except (Exception, KeyboardInterrupt) as e:
        print(f"Processing stopped because of '{results}'")
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(repos))
