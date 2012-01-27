"""Award achievements to players for making comments on github pull requests,
and bonuses for receiving comments with the :sparkles: emoticon added to
indicate good work.
"""
from datetime import datetime

from devrace import redis, settings
from devrace.contest import Achievement
from devrace.github import GitPullRequestsClient

SPARKLES = ':sparkles:'
PULL_UPDATED_KEY = 'GITTRIAL:updated:%s'
SEEN_COMMENTS_KEY = 'GITTRIAL:comments:%s'

def _reset_trial():
    for key in redis.keys('GITTRIAL*'):
        redis.delete(key)

def get_author(obj, players):
    author = obj['user']['login']
    for player in players:
        if player.github_login == author:
            return player
    return None

def award_comment_achievements(pull, comment, pull_author, players):
    key = SEEN_COMMENTS_KEY % pull['number']
    if redis.sismember(key, comment['id']):
        print 'seen comment previously'
        return

    comment_author = get_author(comment, players)
    print 'comment author:', comment_author
    if comment_author and comment_author != pull_author:
        print 'points for commenting'
        comment_author.achievements.append(Achievement(1))

    if (pull_author and comment_author != pull_author
        and SPARKLES in comment['body']):
        print 'bonus:', comment['body']
        pull_author.achievements.append(Achievement(4))

    redis.sadd(key, comment['id'])

class PullRequestTrial(object):
    def __init__(self, git_user, repo_name):
        self.git_user = git_user
        self.repo_name = repo_name
        self.client = GitPullRequestsClient(settings.GIT_USER, settings.GIT_PASS)

    def analyze_pull_request(self, pull, players):
        """Check whether we have seen this pull request before, and if so,
        whether it has changed. If there's potentially new information here,
        get the comments and analyze them.
        """
        print 'inspecting', pull['number']
        key = PULL_UPDATED_KEY % pull['number']
        updated = redis.get(key)
        print updated
        if updated and updated == pull['updated_at']:
            return

        author = get_author(pull, players)
        for comment in self.client.get_pull_request_comments(self.git_user,
                 self.repo_name, pull['number']):
            award_comment_achievements(pull, comment, author, players)

        redis.set(key, pull['updated_at'])

    def __call__(self, contest):
        for pull in self.client.recent_pull_requests(self.git_user, self.repo_name):
            self.analyze_pull_request(pull, contest.players)

