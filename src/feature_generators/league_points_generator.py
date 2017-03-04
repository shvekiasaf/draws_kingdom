from feature_generators.general_generator import GeneralGenerator


class LeaguePointsGenerator(GeneralGenerator):
    """A generator that adds the current league points for every team in a game.
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

        sorted_game_list_df = game_list.games_df.sort_values(by="Date")

        for index, row in sorted_game_list_df.iterrows():

            home_team_key = row["HomeTeam"] + row["SeasonId"]
            away_team_key = row["AwayTeam"] + row["SeasonId"]

            if home_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[home_team_key] = 0

            if away_team_key not in season_id_team_points_dic:
                season_id_team_points_dic[away_team_key] = 0

            game_list.games_df.loc[int(row.name), "HomeTeamLeaguePoints"] = season_id_team_points_dic[home_team_key]
            game_list.games_df.loc[int(row.name), "AwayTeamLeaguePoints"] = season_id_team_points_dic[away_team_key]

            if row["FTHG"] > row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 3
            elif row["FTHG"] == row["FTAG"]:
                season_id_team_points_dic[home_team_key] += 1
                season_id_team_points_dic[away_team_key] += 1
            else:
                season_id_team_points_dic[away_team_key] += 3

        return game_list
