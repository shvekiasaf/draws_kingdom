from feature_generators.general_generator import GeneralGenerator


# grades games by the difference between the average scoring of home and away teams, based on the history of home and
# and away scoring. Read with caution, uses the power of the data frame groupby, sum and count functions
class GoalsDifferenceGenerator(GeneralGenerator):
    def inner_calculate_feature(self, game_list):
        for index, game in game_list.games_df.iterrows():
            previous_games = GeneralGenerator.filter_games_before_date(self, game_list, game['Date'])
            home_team_never_played_at_home = game['AwayTeam'] not in previous_games.AwayTeam.values
            away_team_never_played_away = game['HomeTeam'] not in previous_games.HomeTeam.values
            if previous_games.empty or home_team_never_played_at_home or away_team_never_played_away:
                scoring_distance = -1
            else:
                home_team__mean = previous_games.groupby('HomeTeam').mean()
                away_team__mean = previous_games.groupby('AwayTeam').mean()
                scoring_distance = abs(home_team__mean['FTHG'][game['HomeTeam']] -
                                       away_team__mean['FTAG'][game['AwayTeam']])
            game_list.games_df.loc[int(game.name), 'ScoringDistance'] = scoring_distance
        return game_list
