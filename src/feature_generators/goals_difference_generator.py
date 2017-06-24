from feature_generators.general_generator import GeneralGenerator
import pandas
import datetime


# grades games by the difference between the average scoring of home and away teams, based on the history of home and
# and away scoring. Read with caution, uses the power of the data frame groupby, sum and count functions
class GoalsDifferenceGenerator(GeneralGenerator):

    def inner_calculate_feature(self, game_list):
        minus_one_games = 0
        previous_games = pandas.DataFrame(columns=game_list.games_df.columns, dtype=float)
        for index, game in game_list.games_df.sort_values(by="Date").iterrows():

            if self.period:
                previous_games = previous_games[previous_games.Date >= game.Date - datetime.timedelta(days=self.period)]

            home_team_never_played_home = game.HomeTeam not in previous_games.HomeTeam.values
            away_team_never_played_away = game.AwayTeam not in previous_games.AwayTeam.values

            if previous_games.empty or (home_team_never_played_home and away_team_never_played_away):
                game_list.games_df.loc[int(game.name), self.get_printable_name()] = -1
                minus_one_games += 1
            else:
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
                game_list.games_df.loc[int(game.name), self.get_printable_name()] = abs(
                    home_team_mean['FTHG'][game[team_for_home_team]] -
                    away_team_mean['FTAG'][game[team_for_away_team]])

            previous_games = previous_games.append(game)
        # print('GoalsDifferenceGenerator missing game ratings ' + str(minus_one_games))
        return game_list

    def get_feature_names(self):
        return [self.get_printable_name()]