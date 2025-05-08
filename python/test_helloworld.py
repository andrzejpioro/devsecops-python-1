import helloworld
if __name__ == '__main__':
    # myapp.getBranchProtectionRules(owner="andrzejpioro",repo="alertmanager-webhook-servicenow", masterBranchName="master")
    # myapp.getBranchProtectionRules(owner="andrzejpioro",repo="artifactory-cleanup", masterBranchName="main")

    # myapp.getProectionRule(username="andrzejpioro", repo="artifactory-cleanup", branch="main")

    print(helloworld.getSecretNamesForRepo("andrzejpioro", "artifactory-cleanup"))
