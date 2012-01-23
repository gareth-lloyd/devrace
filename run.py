from time import sleep
from serial.serialutil import SerialException
from datetime import datetime

from devrace.git_trial import PullRequestTrial, _reset_trial
from devrace.contest import Contest, Player
from devrace.scoreboard import PeggyScoreboard, PrintingScoreboard

if __name__ == '__main__':
    _reset_trial()

    players = [
        Player('gareth', {'github_login': 'gareth-lloyd'}),
        Player('colin', {'github_login': 'colinhowe'}),
        Player('christy', {'github_login': 'c-oreills'}),
        Player('james', {'github_login': 'jmslovatt'}),
        Player('henrique', {'github_login': 'hjrnunes'}),
        Player('gehan', {'github_login': 'gehan'}),
    ]
    trials = [
        PullRequestTrial('conversocial', 'conversocial')
    ]
    contest = Contest(players, trials)
    try:
        scoreboard = PeggyScoreboard()
    except SerialException:
        scoreboard = PrintingScoreboard()

    while True:
        contest.run_trials()
        for player in players:
            print player.name, ':', len(player.achievements)
        scoreboard.update_scores(contest)
        sleep(10)
