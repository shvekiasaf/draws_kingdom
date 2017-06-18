from feature_generators.general_generator import GeneralGenerator


# grades games by the difference between the average scoring of home and away teams, based on the history of home and
# and away scoring. Read with caution, uses the power of the data frame groupby, sum and count functions
class GoalsDifferenceGenerator(GeneralGenerator):
    def inner_calculate_feature(self, game_list):
        minus_one_games = 0
        for index, game in game_list.games_df.iterrows():
            previous_games = GeneralGenerator.filter_games_before_date(self, game_list, game['Date'])
            home_team_never_played_home = game.HomeTeam not in previous_games.HomeTeam.values
            away_team_never_played_away = game.AwayTeam not in previous_games.AwayTeam.values

            if previous_games.empty or (home_team_never_played_home and away_team_never_played_away):
                game_list.games_df.loc[int(game.name), 'ScoringDistance'] = -1
                minus_one_games += 1
                continue

            if home_team_never_played_home:
                # if home team never played at home, we take the average scoring against the away team when they
                # play away
                home_team_mean = previous_games.groupby('AwayTeam').mean()
                team_for_home_team = 'AwayTeam'
            else:
                home_team_mean = previous_games.groupby('HomeTeam').mean()
                team_for_home_team = 'HomeTeam'

            if away_team_never_played_away:
                # if away team never played away, we take the average scoring against the home team when they
                # play at home
                away_team_mean = previous_games.groupby('HomeTeam').mean()
                team_for_away_team = 'HomeTeam'
            else:
                away_team_mean = previous_games.groupby('AwayTeam').mean()
                team_for_away_team = 'AwayTeam'

            scoring_distance = abs(home_team_mean['FTHG'][game[team_for_home_team]] -
                                   away_team_mean['FTAG'][game[team_for_away_team]])
            game_list.games_df.loc[int(game.name), 'ScoringDistance'] = scoring_distance
        # print('GoalsDifferenceGenerator missing game ratings ' + str(minus_one_games))
        return game_list
