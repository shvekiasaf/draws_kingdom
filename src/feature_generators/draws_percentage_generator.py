from feature_generators.general_generator import GeneralGenerator
import pandas
import datetime


class DrawsPercentageGenerator(GeneralGenerator):
    """The generator calculates the draw ratio for each team, and grades each game by the average of both team ratios.
    Note: needs to run after @league_points_generator"""

    def inner_calculate_feature(self, game_list):
        previous_games = pandas.DataFrame(columns=game_list.games_df.columns)

        for index, game in game_list.games_df.sort_values(by="Date").iterrows():

            if self.period:
                previous_games = previous_games[previous_games.Date >= game.Date - datetime.timedelta(days=self.period)]

            games_with_either_team = previous_games[
                (previous_games.HomeTeam == game.HomeTeam) |
                (previous_games.HomeTeam == game.AwayTeam) |
                (previous_games.AwayTeam == game.HomeTeam) |
                (previous_games.AwayTeam == game.AwayTeam)]

            if games_with_either_team.empty:
                game_list.games_df.loc[
                    int(game.name), self.get_printable_name()] = -1
            else:
                # we simply use Div to get the count. All other columns would also work
                total_games_with_teams = games_with_either_team.count()['Div']
                number_of_draws_for_teams = games_with_either_team[games_with_either_team.Draw].count()['Div']

                game_list.games_df.loc[
                    int(game.name), self.get_printable_name()] = number_of_draws_for_teams / total_games_with_teams

            previous_games = previous_games.append(game)

        return game_list

    def get_feature_names(self):
        return [self.get_printable_name()]