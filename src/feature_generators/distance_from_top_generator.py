from feature_generators.general_generator import GeneralGenerator


class DistanceFromTopGenerator(GeneralGenerator):
    """The generator calculate the average distance from the top of the table, and add it as a feature
    we normalize the distance with the number of games actually played so far.
    Relies on LeaguePointsGenerator"""

    def inner_calculate_feature(self, game_list):

        sorted_game_list_df = game_list.games_df.sort_values(by="Date")
        max_points = {}  # holds the number of points for top team per league

        for index, row in sorted_game_list_df.iterrows():

            if row["SeasonId"] not in max_points:
                max_points[row["SeasonId"]] = 0

            if game_list.games_df.loc[int(row.name), "HomeTeamGamesPlayedInSeason"] == 0 and \
               game_list.games_df.loc[int(row.name), "AwayTeamGamesPlayedInSeason"] == 0:

                game_list.games_df.loc[int(row.name), "DistanceFromTop"] = 0

            else:

                # update top points if needed
                top_team_points = max(game_list.games_df.loc[int(row.name), "HomeTeamLeaguePoints"],
                                      game_list.games_df.loc[int(row.name), "AwayTeamLeaguePoints"])
                max_points[row["SeasonId"]] = max(top_team_points, max_points[row["SeasonId"]])

                distance_from_top = ((2 * max_points[row["SeasonId"]]) -
                                     game_list.games_df.loc[int(row.name), "HomeTeamLeaguePoints"] -
                                     game_list.games_df.loc[int(row.name), "AwayTeamLeaguePoints"]) / 2
                games_played = (game_list.games_df.loc[int(row.name), "HomeTeamGamesPlayedInSeason"] +
                                game_list.games_df.loc[int(row.name), "AwayTeamGamesPlayedInSeason"]) / 2

                normalized_distance_from_top = distance_from_top / games_played
                game_list.games_df.loc[int(row.name), "DistanceFromTop"] = normalized_distance_from_top

        return game_list

    def get_feature_names(self):
        return ["DistanceFromTop"]
