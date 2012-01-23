import requests
import json
from datetime import datetime

API_URL = 'https://api.github.com/'
PULLS_PATH = 'repos/%s/%s/pulls'
D_FMT = '%Y-%m-%dT%H:%M:%SZ'

def d(date_string):
    return datetime.strptime(date_string, D_FMT)

class GitPullRequestsClient(object):
    """Super simple API client that just uses basic auth to make requests
    and return json objects.
    """
    def __init__(self, username, password):
        self.username = username
        self._session = requests.session()
        self._session.auth = (username, password)
        self._session.headers.update({'Accept': 'application/json'})

    def api_call(self, path):
        r = self._session.get(API_URL + path)
        r.raise_for_status()
        return json.loads(r.content)

    def get_pull_requests(self, username, repo, closed=False):
        path = PULLS_PATH % (username, repo)
        if closed:
            path += '?state=closed'
        return self.api_call(path)

    def recent_pull_requests(self, username, repo):
        pulls = self.get_pull_requests(username, repo)
        pulls.extend(self.get_pull_requests(username, repo, closed=True))
        return pulls

    def get_pull_request_comments(self, username, repo, pull_number):
        path = PULLS_PATH + '/%s/comments'
        return self.api_call(path % (username, repo, pull_number))
