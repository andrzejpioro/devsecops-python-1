import helloworld
if __name__ == '__main__':
    helloworld.getBranchProtectionRules(owner="andrzejpioro",repo="alertmanager-webhook-servicenow", masterBranchName="master")

    print(helloworld.getSecretNamesForRepo("andrzejpioro", "artifactory-cleanup"))
