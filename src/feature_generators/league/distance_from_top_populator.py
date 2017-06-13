from feature_generators.league.base_metric_populator import BaseMetricPopulator, get_team_key


# here we calculate the average distance from the top of the table, and add it as a feature
# note we normalize the distance with the number of games actually played so far
class DistanceFromTopPopulator(BaseMetricPopulator):
    def update_metric(self, game_list, max_points, number_of_games_played, row, season_id_team_points_dic):

        home_team_key = get_team_key(row, "HomeTeam")
        away_team_key = get_team_key(row, "AwayTeam")

        if number_of_games_played[home_team_key] == 0 and number_of_games_played[away_team_key] == 0:
            game_list.games_df.loc[int(row.name), "DistanceFromLeader"] = -1
            return

        # update top points if needed
        top_team_points = max(season_id_team_points_dic[home_team_key], season_id_team_points_dic[away_team_key])
        max_points[row["SeasonId"]] = max(top_team_points, max_points[row["SeasonId"]])

        distance_from_top = ((2 * max_points[row["SeasonId"]]) - season_id_team_points_dic[home_team_key] -
                             season_id_team_points_dic[away_team_key]) / 2
        games_played = (number_of_games_played[home_team_key] + number_of_games_played[away_team_key]) / 2
        normalized_distance_from_top = distance_from_top / games_played
        game_list.games_df.loc[int(row.name), "DistanceFromLeader"] = normalized_distance_from_top
