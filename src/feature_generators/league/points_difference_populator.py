from feature_generators.league.base_metric_populator import BaseMetricPopulator, get_team_key


class PointsDifferencePopulator(BaseMetricPopulator):
    def update_metric(self, game_list, max_points, number_of_games_played, row, season_id_team_points_dic):
        game_list.games_df.loc[int(row.name), "LeaguePointsDiff"] = abs(
            season_id_team_points_dic[get_team_key(row, "HomeTeam")] -
            season_id_team_points_dic[get_team_key(row, "HomeTeam")])
