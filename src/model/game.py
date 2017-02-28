class Game:
    """Represents a game"""

    def __init__(self, home_team, away_team, home_score, away_score, division, date, season, league_name):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.division = division
        self.date = date
        self.season = season
        self.league_name = league_name
        self.home_team_league_points = 0
        self.away_team_league_points = 0

        self.seasonId = self.league_name + self.season + self.division