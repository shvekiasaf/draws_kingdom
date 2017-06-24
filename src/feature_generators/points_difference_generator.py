from feature_generators.general_generator import GeneralGenerator


class PointsDifferenceGenerator(GeneralGenerator):
    """The generator adds the point differences between the to teams in the league.
    Relies on LeaguePointsGenerator"""

    def inner_calculate_feature(self, game_list):

        game_list.games_df["LeaguePointsDiff"] = abs(
            game_list.games_df["HomeTeamLeaguePoints"] - game_list.games_df["AwayTeamLeaguePoints"])

        return game_list

    def get_feature_names(self):
        return ["LeaguePointsDiff"]
