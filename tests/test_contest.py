from unittest import TestCase
from mock import Mock
from devrace.contest import Player, Contest

class PlayerTests(TestCase):
    def setUp(self):
        self.player = Player('name', {})

    def test_calculate_score_empty(self):
        self.assertEquals(0, self.player.current_score)

    def test_score_with_one_achievement(self):
        mock_achievement = Mock()
        mock_achievement.points_value = 2
        self.player.achievements.append(mock_achievement)
        self.assertEquals(2, self.player.current_score)

    def test_achievement_values_are_added(self):
        mock_achievement1 = Mock()
        mock_achievement1.points_value = 2
        self.player.achievements.append(mock_achievement1)
        mock_achievement2 = Mock()
        mock_achievement2.points_value = 3
        self.player.achievements.append(mock_achievement2)
        self.assertEquals(5, self.player.current_score)

    def test_player_options(self):
        player = Player('name', {'opt_name': 'opt_value'})
        self.assertEquals('name', player.name)
        self.assertEquals('opt_value', player.opt_name)

class ContestTests(TestCase):
    def setUp(self):
        players = [
            Player('player1', {}),
            Player('player2', {}),
        ]
        self.contest = Contest(players, [])

    def test_update(self):
        mock_achievement = Mock()
        mock_achievement.points_value = 2
        def mock_trial(contest):
            for player in contest.players:
                player.achievements.append(mock_achievement)
        self.contest.trials.append(mock_trial)
        self.contest.run_trials()

        self.assertEquals(2, self.contest.players[0].current_score)

