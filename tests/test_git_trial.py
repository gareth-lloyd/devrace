from datetime import datetime

from unittest import TestCase
from mock import Mock
from devrace.git_trial import (get_author, award_comment_achievements,
       PullRequestTrial, _reset_trial)
from devrace.contest import Player

class GitTrialTests(TestCase):
    def setUp(self):
        _reset_trial()
        self.players = [
            Player('a', {'github_login': 'c-oreills'}),
            Player('b', {'github_login': 'gareth-lloyd'})
        ]

    def test_get_author(self):
        pull = {'user':{'login': 'c-oreills'}}
        self.assertEquals(self.players[0], get_author(pull, self.players))

    def test_get_author_not_present(self):
        pull = {'user':{'login': 'someguy'}}
        self.assertEquals(None, get_author(pull, self.players))

    def test_cannot_award_to_self(self):
        pull = {'number': 1}
        comment = {'id': 3, u'body': u':sparkles:', 'user':{'login': 'c-oreills'}}
        pull_author = self.players[0]
        award_comment_achievements(pull, comment, pull_author, self.players)
        self.assertEquals(0, len(pull_author.achievements))

    def test_can_award_bonus_to_others(self):
        pull = {'number': 1}
        comment = {'id': 4, u'body': u':sparkles:', 'user':{'login': 'c-oreills'}}
        pull_author = self.players[1]
        award_comment_achievements(pull, comment, pull_author, self.players)
        self.assertEquals(1, len(pull_author.achievements))

    def test_receive_points_for_commenting(self):
        pull = {'number': 1}
        comment = {'id': 5, u'body': u':sparkles:', 'user':{'login': 'c-oreills'}}
        pull_author = self.players[1]
        award_comment_achievements(pull, comment, pull_author, self.players)
        comment_author = self.players[0]
        self.assertEquals(1, len(comment_author.achievements))

