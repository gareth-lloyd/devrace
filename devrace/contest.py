"""A very basic framework for running contests between players.
"""

class Player(object):
    def __init__(self, name, options):
        self.achievements = []
        self.name = name
        self.options = options

    @property
    def current_score(self):
        return sum([a.points_value for a in self.achievements])

    def __getattr__(self, name):
        return self.options.get(name, None)

class Contest(object):
    def __init__(self, players, trials):
        self.players = players
        self.trials = trials

    def run_trials(self):
        for trial in self.trials:
            trial(self)

class Achievement(object):
    def __init__(self, points_value):
        self.points_value = points_value
