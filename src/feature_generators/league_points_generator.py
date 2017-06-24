from numpy import math

from feature_generators.general_generator import GeneralGenerator


def is_nan(x):
    return isinstance(x, float) and math.isnan(x)


class LeaguePointsGenerator(GeneralGenerator):
    """The generator adds the current league points for every team in a game.
    New features: HomeTeamLeaguePoints and AwayTeamLeaguePoints"""

    def inner_calculate_feature(self, game_list):

        season_id_team_points_dic = {}

        game_list.games_df["HomeTeamLeaguePoints"] = -1
        game_list.games_df["AwayTeamLeaguePoints"] = -1
        game_list.games_df["HomeTeamGamesPlayedInSeason"] = -1
        game_list.games_df["AwayTeamGamesPlayedInSeason"] = -1

        sorted_game_list_df = game_list.games_df.sort_values(by="Date")

        number_of_games_played = {}

        for index, row in sorted_game_list_df.iterrows():

            home_team_key = row["HomeTeam"] + row["SeasonId"]
            away_team_key = row["AwayTeam"] + row["SeasonId"]

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
            game_list.games_df.loc[int(row.name), "HomeTeamGamesPlayedInSeason"] = number_of_games_played[home_team_key]
            game_list.games_df.loc[int(row.name), "AwayTeamGamesPlayedInSeason"] = number_of_games_played[away_team_key]

            number_of_games_played[home_team_key] += 1
            number_of_games_played[away_team_key] += 1

            if row["FTHG"] > row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 3
            elif row["FTHG"] == row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 1
                season_id_team_points_dic[away_team_key] += 1
            else:
                season_id_team_points_dic[away_team_key] += 3

        return game_list

    def get_feature_names(self):
        return ["HomeTeamLeaguePoints", "AwayTeamLeaguePoints",
                "HomeTeamGamesPlayedInSeason", "AwayTeamGamesPlayedInSeason"]
