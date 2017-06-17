from feature_generators.general_generator import GeneralGenerator


# grades games by the difference between the average scoring of home and away teams, based on the history of home and
# and away scoring. Read with caution, uses the power of the data frame groupby, sum and count functions
class GoalsDifferenceGenerator(GeneralGenerator):
    def inner_calculate_feature(self, game_list):
        home_team__mean = game_list.games_df.groupby('HomeTeam').mean()
        away_team__mean = game_list.games_df.groupby('AwayTeam').mean()
        for index, game in game_list.games_df.iterrows():
            game_list.games_df.loc[int(game.name), 'ScoringDistance'] = abs(home_team__mean['FTHG'][game['HomeTeam']] -
                                                                            away_team__mean['FTAG'][game['AwayTeam']])
        return game_list
