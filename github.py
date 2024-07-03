import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):

    # Craft URL
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"

    # Make request
    headers = {"Authorization": f"Bearer {github_token}"}
    response = requests.get(url, headers=headers)

    # Successful request
    if response.status_code == 200:
        data = response.json() # Dictionary 
    else:
        print("Failed with status code:", response.status_code)
        return []

    print(data)
    return data


def fetch_github_issues(owner, repo):
    data = fetch_github(owner, repo, "issues")
    return load_issues(data)


def load_issues(issues):
    """
    Load issues into Langchain Document objects to use in RAG
    """
    docs = []

    # Iterate through issues
    for entry in issues:
        # Extract metadata into dictionary
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            "body": entry["body"],
            "labels": entry["labels"],
            "created_at": entry["created_at"],
        }
        data = entry["title"]
        if entry["body"]:
            data += entry["body"]
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)

    return docs


owner = "techwithtim"
repo = "Flask-Web-App-Tutorial"
endpoint = "issues"
fetch_github_issues(owner, repo)