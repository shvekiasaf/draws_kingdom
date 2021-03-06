from feature_generators.base_per_league_goals_normalized_generator import BaseLeagueGoalsNormalizedGenerator


class LeagueGoalsDifferenceNormalizedGenerator(BaseLeagueGoalsNormalizedGenerator):
    def get_game_grade(self, home_team_score, away_team_score):
        return abs(home_team_score - away_team_score)
