import requests
import base64
import git
import os

TOKEN_LOC = "token.txt"
URL = "gitea:3000"
HOST = "http://"+URL

def create_user(user, passwd):
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "lang=en-US; i_like_gitea=8e2779a79e7d3e28; _csrf=uBwdvQ2EKSS69kVzPIGOPI1OmoU6MTU5NDMxMTk2NzA1ODIxMjgzNw"
    }
    data = {
        "user_name": user,
        "email": f"{user}@gisac.acm",
        "password": passwd,
        "retype": passwd,
    }

    response = requests.post(HOST+'/user/sign_up', headers=headers, data=data)
    if response.status_code == 200:
        print(f"User {user} created successfully.")
    else:
        print(f"Failed to create user {user}. Status code: {response.status_code}")
        print(response.text)

def create_repo(repo, user, passwd):
    auth = base64.b64encode(f'{user}:{passwd}'.encode()).decode('utf-8')

    headers = {
        'accept': 'application/json',
        'authorization': 'Basic '+auth,
        'Content-Type': 'application/json'
    }

    data ={
    "auto_init": False,
    "default_branch": "master",
    "description": "",
    "gitignores": "",
    "issue_labels": "",
    "license": "MIT",
    "name": repo,
    "object_format_name": "sha1",
    "private": False,
    "readme": "",
    "template": False,
    "trust_model": "default"
    }

    response = requests.post(HOST+'/api/v1/user/repos', headers=headers, json=data)
    if response.status_code == 201:
        print(f"Repository {repo} created successfully.")
    else:
        print(f"Failed to create repository {repo}. Status code: {response.status_code}")
        print(response.text)


    headers = {
        'accept': 'application/json',
        'authorization': 'Basic '+auth,
        'Content-Type': 'application/json'
    }
    return f"{URL}/{user}/{repo}.git"

def create_token(user, passwd):
    auth = base64.b64encode(f'{user}:{passwd}'.encode()).decode('utf-8')
    headers = {
        'accept': 'application/json',
        'authorization': 'Basic '+auth,
        'Content-Type': 'application/json'
    }
    data = {
        "name": os.urandom(16).hex(),
        "scopes": [
            "write:repository"
        ]
    }

    response = requests.post(HOST+f'/api/v1/users/{user}/tokens', headers=headers, json=data)

    token = response.json()['sha1']
    with open(TOKEN_LOC, 'w') as f:
        f.write(token)
    return token

user = "gisac_deploy"
passwd = '52aa1dc095038e8b'

create_user(user, passwd)
backup_repo = create_repo("backup_gen", user, passwd)
exec_repo = create_repo("ejecutor", user, passwd)
token = create_token(user, passwd)

REPO_PATH = "./.watching"





repo_ = git.Repo(REPO_PATH)

part = f"http://{user}:{token}@"


try:
    repo_ = repo_.create_remote("origin", part+backup_repo)
except:
    repo_ = repo_.remote().set_url(part+backup_repo)
finally:
    repo_.push('master')
    repo_.push('dev')


REPO_PATH = "./executer"
repo_ = git.Repo(REPO_PATH)
try:
    repo_ = repo_.create_remote("origin", part+exec_repo)
except:
    repo_ = repo_.remote().set_url(part+exec_repo)
finally:
    repo_.push('master')