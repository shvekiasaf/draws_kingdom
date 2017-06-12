from feature_generators.general_generator import GeneralGenerator


class LeaguePointsGenerator(GeneralGenerator):
    """The generator adds the current league points for every team in a game.
    New features: HomeTeamLeaguePoints and AwayTeamLeaguePoints"""

    def calculate_feature(self, game_list):

        if game_list is None:
            return game_list
        elif game_list.games_df is None:
            return game_list
        elif game_list.games_df.empty:
            return game_list

        season_id_team_points_dic = {}

        game_list.games_df["HomeTeamLeaguePoints"] = -1
        game_list.games_df["AwayTeamLeaguePoints"] = -1
        game_list.games_df["LeaguePointsDiff"] = -1

        sorted_game_list_df = game_list.games_df.sort_values(by="Date")
        # holds the number of points for top team per league
        max_points = {}
        number_of_games_played = {}

        for index, row in sorted_game_list_df.iterrows():

            home_team_key = row["HomeTeam"] + row["SeasonId"]
            away_team_key = row["AwayTeam"] + row["SeasonId"]

            if row["SeasonId"] not in max_points:
                max_points[row["SeasonId"]] = 0

            if home_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[home_team_key] = 0

            if away_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[away_team_key] = 0

            if home_team_key not in number_of_games_played:
                number_of_games_played[home_team_key] = 0

            if away_team_key not in number_of_games_played:
                number_of_games_played[away_team_key] = 0

            game_list.games_df.loc[int(row.name), "HomeTeamLeaguePoints"] = season_id_team_points_dic[home_team_key]
            game_list.games_df.loc[int(row.name), "AwayTeamLeaguePoints"] = season_id_team_points_dic[away_team_key]
            game_list.games_df.loc[int(row.name), "LeaguePointsDiff"] = abs(season_id_team_points_dic[away_team_key] -
                                                                            season_id_team_points_dic[home_team_key])

            if row["FTHG"] > row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 3
            elif row["FTHG"] == row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 1
                season_id_team_points_dic[away_team_key] += 1
            else:
                season_id_team_points_dic[away_team_key] += 3

            number_of_games_played[home_team_key] += 1
            number_of_games_played[away_team_key] += 1

            self.calculate_distance_from_top(away_team_key, game_list, home_team_key, max_points, number_of_games_played,
                                             row, season_id_team_points_dic)

        return game_list

    # here we calculate the average distance from the top of the table, and add it as a feature
    # note we normalize the distance with the number of games actually played so far
    def calculate_distance_from_top(self, away_team_key, game_list, home_team_key, max_points, number_of_games_played, row,
                                    season_id_team_points_dic):
        # update top points if needed
        top_team_points = max(season_id_team_points_dic[home_team_key], season_id_team_points_dic[away_team_key])
        max_points[row["SeasonId"]] = max(top_team_points, max_points[row["SeasonId"]])

        distance_from_top = ((2 * max_points[row["SeasonId"]]) - season_id_team_points_dic[home_team_key] -
                             season_id_team_points_dic[away_team_key]) / 2
        normalized_distance_from_top = distance_from_top / number_of_games_played[home_team_key]
        game_list.games_df.loc[int(row.name), "DistanceFromLeader"] = normalized_distance_from_top
