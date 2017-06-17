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

    @staticmethod
    def get_scoring_avg(game, team_game_count, team_sum, team, scoring_column):
        team_goal_count = team_sum.loc[game[team]].loc[scoring_column]
        num_of_games = team_game_count['Div'].loc[game[team]]
        home_team_scoring_avg = team_goal_count / num_of_games
        return home_team_scoring_avg
