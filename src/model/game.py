class Game:
    """Represents a game"""

    def __init__(self, home_team, away_team, home_score, away_score, division, date, season):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.division = division
        self.date = date
        self.season = season