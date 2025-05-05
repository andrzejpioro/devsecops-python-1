# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests

from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("access_token")


hostName = "localhost"
serverPort = 8080

accountToCheck = "https://api.github.com/users/bregman-arie/repos"

userToCheck = "bregman-arie"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        # Public Web Github
        g = Github()
        user = g.get_user(userToCheck)
        repos = user.get_repos()
          

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>DevSecOps</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Hello World</p>", "utf-8"))
        for repo in repos:
            self.wfile.write(bytes("<p>"+repo+"</p>"))
            

        self.wfile.write(bytes("</body></html>", "utf-8"))


def userexists(username):
    addr = "https://api.github.com/users/" + username
    response = requests.get(addr)
    if response.status_code == 404:
        return False
    else:
        if response.status_code == 200:
            return True

def printrepos(repos):
        original_repos = []
        for repo in repos:
            if repo.fork is False and repo.archived is False:
                print(repo.clone_url)




if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")