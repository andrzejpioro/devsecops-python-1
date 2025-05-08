from flask import Flask, render_template, request
import json
import requests
import os

app = Flask(__name__)

accountToCheck = "andrzejpioro"


@app.route('/healthz')
def healthz():
    return "OK", 200

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    username = request.args.get('username', accountToCheck)
    print ("User from arg: "+username)
    repos = getRepoDetailsForAccount(username)
    return render_template("repos.html", username=username, repos=repos, title="Repos for user: "+username)



def getRepoDetailsForAccount(username):
    repos = getRepoForUser(username)
    print("Repos: " +json.dumps(repos, indent=2))
    reposDetails = []
    for repo in repos:
        name = repo["name"]
        url = repo["url"]
        defaultBranch = repo["default_branch"]
        branchProtectionRules = getBranchProtectionRules(username,name,defaultBranch)
        print(f"Branch protection rule for repo=[{name}]: {json.dumps(branchProtectionRules,indent=2)}")
        secrets = getSecretNamesForRepo(username,name)

        if branchProtectionRules:
            deletionAllowed = branchProtectionRules["allow_deletions"]["enabled"]
            forcePushAllowed = branchProtectionRules["allow_force_pushes"]["enabled"]
        else:
            deletionAllowed = True
            forcePushAllowed = True

        repoDetail = {
            "name" : name,
            "url" : url,
            "default_branch" : defaultBranch,
            "deletion_allowed" : deletionAllowed,
            "force_push_allowed" : forcePushAllowed,
            "secrets" : secrets
        }
        reposDetails.append(repoDetail)
    print("###############")
    print(reposDetails)
    return reposDetails




def listSecretForRepo(owner, repo):
    print (f"listSecretForRepo owner=[{owner}], repo=[{repo}]")
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/actions/secrets", headers=getAuth())
    if response.status_code == 404:
        return None
    elif response.status_code == 403:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
        print(f"ERROR - listSecretForRepo failed for {owner} - {repo}")
        return []



def getSecretNamesForRepo(owner,repo):
    secretsJson = listSecretForRepo(owner,repo)
    if secretsJson:
        secrets = secretsJson['secrets']
        sercetNames = []
        for secret in secretsJson["secrets"]:
            sercetNames.append(secret["name"])
        return sercetNames
    else:
        return []


def getBranchProtectionRules(owner,repo, masterBranchName):
    print(f"GetBranchProtectionRule: owner={owner}, repo={repo} + branch={masterBranchName}")
    response = requests.get(f'https://api.github.com//repos/{owner}/{repo}/branches/{masterBranchName}/protection', headers=getAuth())
    if (response.status_code == 404):
        return None
    if response.status_code == 200:
        print(json.dumps(response.json(),indent=2))
        return response.json()
    else:
        print(f"There is a problem with getting info about protection: owner={owner}, repo={repo}, masterBranch={masterBranchName}")


def getRepoForUser(username):
    response = requests.get(f'https://api.github.com/users/{username}/repos', headers=getAuth())
    print(response)
    if response.status_code == 200:
        repos = response.json()
    else:
        repos = []  
    
    return repos



def getAuth():
    githubToken = os.environ.get('GITHUB_TOKEN')
    headers  = {'Authorization': 'Bearer '+githubToken}
    return headers


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port="5001")
