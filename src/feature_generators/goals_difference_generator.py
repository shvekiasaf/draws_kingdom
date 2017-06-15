from feature_generators.general_generator import GeneralGenerator


# grades games by the difference between the average scoring of home and away teams, based on the history of home and
# and away scoring. Read with caution, uses the power of the data frame groupby, sum and count functions
class GoalsDifferenceGenerator(GeneralGenerator):
    def inner_calculate_feature(self, game_list):
        home_team_sum = game_list.games_df.groupby('HomeTeam').sum()
        away_team_sum = game_list.games_df.groupby('AwayTeam').sum()
        home_team_game_count = game_list.games_df.groupby('HomeTeam').count()
        away_team_game_count = game_list.games_df.groupby('AwayTeam').count()

        for index, game in game_list.games_df.iterrows():
            home_team_scoring_avg = self.get_scoring_avg(game, home_team_game_count, home_team_sum, 'HomeTeam', 'FTHG')
            away_team_scoring_avg = self.get_scoring_avg(game, away_team_game_count, away_team_sum, 'AwayTeam', 'FTAG')
            game_list.games_df.loc[int(game.name), 'ScoringDistance'] = abs(home_team_scoring_avg -
                                                                            away_team_scoring_avg)

    @staticmethod
    def get_scoring_avg(game, team_game_count, team_sum, team, scoring_column):
        team_goal_count = team_sum.loc[game[team]].loc[scoring_column]
        num_of_games = team_game_count['Div'].loc[game[team]]
        home_team_scoring_avg = team_goal_count / num_of_games
        return home_team_scoring_avg