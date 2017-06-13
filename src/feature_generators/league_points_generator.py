from numpy import math

from feature_generators.general_generator import GeneralGenerator
from feature_generators.league.distance_from_top_populator import DistanceFromTopPopulator
from feature_generators.league.points_difference_populator import PointsDifferencePopulator


def is_nan(x):
    return isinstance(x, float) and math.isnan(x)


class LeaguePointsGenerator(GeneralGenerator):
    """The generator adds the current league points for every team in a game.
    New features: HomeTeamLeaguePoints and AwayTeamLeaguePoints"""

    def inner_calculate_feature(self, game_list):

        if game_list is None:
            return game_list
        elif game_list.games_df is None:
            return game_list
        elif game_list.games_df.empty:
            return game_list

        metric_populators = [PointsDifferencePopulator(), DistanceFromTopPopulator()]

        season_id_team_points_dic = {}

        game_list.games_df["HomeTeamLeaguePoints"] = -1
        game_list.games_df["AwayTeamLeaguePoints"] = -1
        game_list.games_df["LeaguePointsDiff"] = -1

        sorted_game_list_df = game_list.games_df.sort_values(by="Date")
        # holds the number of points for top team per league
        max_points = {}
        number_of_games_played = {}

        for index, row in sorted_game_list_df.iterrows():

            if is_nan(row["HomeTeam"]) or is_nan(row["AwayTeam"]):
                continue

            home_team_key = row["HomeTeam"] + row["SeasonId"]
            away_team_key = row["AwayTeam"] + row["SeasonId"]

            if row["SeasonId"] not in max_points:
                max_points[row["SeasonId"]] = 0

            if home_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[home_team_key] = 0

            if away_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[away_team_key] = 0

            if home_team_key not in number_of_games_played:
                number_of_games_played[home_team_key] = 1
            else:
                number_of_games_played[home_team_key] += 1

            if away_team_key not in number_of_games_played:
                number_of_games_played[away_team_key] = 1
            else:
                number_of_games_played[away_team_key] += 1

            game_list.games_df.loc[int(row.name), "HomeTeamLeaguePoints"] = season_id_team_points_dic[home_team_key]
            game_list.games_df.loc[int(row.name), "AwayTeamLeaguePoints"] = season_id_team_points_dic[away_team_key]

            for populator in metric_populators:
                populator.update_metric(game_list, max_points, number_of_games_played, row, season_id_team_points_dic)

            if row["FTHG"] > row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 3
            elif row["FTHG"] == row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 1
                season_id_team_points_dic[away_team_key] += 1
            else:
                season_id_team_points_dic[away_team_key] += 3

        return game_list
