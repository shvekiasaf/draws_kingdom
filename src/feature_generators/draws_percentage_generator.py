from feature_generators.general_generator import GeneralGenerator


class DrawsPercentageGenerator(GeneralGenerator):
    """The generator calculates the draw ratio for each team, and grades each game by the average of both team ratios.
    Note: needs to run after @league_points_generator"""

    def inner_calculate_feature(self, game_list):

        for index, game in game_list.games_df.iterrows():
            previous_games = GeneralGenerator.filter_games_before_date(self, game_list, game.Date)

            games_with_either_team = previous_games[
                (previous_games.HomeTeam == game.HomeTeam) |
                (previous_games.HomeTeam == game.AwayTeam) |
                (previous_games.AwayTeam == game.HomeTeam) |
                (previous_games.AwayTeam == game.AwayTeam)]

            if games_with_either_team.empty:
                game_list.games_df.loc[
                    int(game.name), "DrawPercentage"] = -1
                continue

            # we simply use Div to get the count. All other columns would also work
            total_games_with_teams = games_with_either_team.count()['Div']
            number_of_draws_for_teams = games_with_either_team[games_with_either_team.Draw].count()['Div']

            game_list.games_df.loc[
                int(game.name), "DrawPercentage"] = number_of_draws_for_teams / total_games_with_teams

        return game_list
