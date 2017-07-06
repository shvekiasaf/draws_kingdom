import pandas as pd

from feature_generators.general_generator import GeneralGenerator


class LowScoringTeamsGenerator(GeneralGenerator):
    """The generator adds the goal difference between the teams
    we normalize the score with the number of games actually played so far.
    Relies on LeaguePointsGenerator"""

    def inner_calculate_feature(self, game_list):

        # calculating the average goals scored so far during that season, both for away and home teams
        scoring_avg_home_team = game_list.games_df["HomeTeamGoalsScoredInSeason"] / \
                                game_list.games_df["HomeTeamGamesPlayedInSeason"]

        scoring_avg_away_team = game_list.games_df["AwayTeamGoalsScoredInSeason"] / \
                                game_list.games_df["AwayTeamGamesPlayedInSeason"]

        # null check
        scoring_avg_home_team[scoring_avg_home_team.isnull()] = 0
        scoring_avg_away_team[scoring_avg_away_team.isnull()] = 0

        # Normalizing:

        # 1. Calculate the average of the proportion of (goals / games played) for both away and home teams
        # on the last game of every season
        home_ratio_series = (game_list.games_df[game_list.games_df.HomeTeamGamesPlayedInSeason ==
                                                (game_list.games_df.MaxGamesPerSeason - 1)]["HomeTeamGoalsScoredInSeason"] /
                             game_list.games_df[game_list.games_df.HomeTeamGamesPlayedInSeason ==
                                                (game_list.games_df.MaxGamesPerSeason - 1)]["MaxGamesPerSeason"])
        away_ratio_series = (game_list.games_df[game_list.games_df.AwayTeamGamesPlayedInSeason ==
                                                (game_list.games_df.MaxGamesPerSeason - 1)]["AwayTeamGoalsScoredInSeason"] /
                             game_list.games_df[game_list.games_df.AwayTeamGamesPlayedInSeason ==
                                                (game_list.games_df.MaxGamesPerSeason - 1)]["MaxGamesPerSeason"])
        global_avg = home_ratio_series.append(away_ratio_series).mean()

        # 2. Grading each team for each game, take into consideration the amount of games.
        # A game with less games will probably be similar to the global average
        #
        # The formula: (global_average * (number_of_games_per_season - number_of_games_so_far) + goal proportion)
        #               ----------------------------------------------------------------------------------------
        #                                           number_of_games_per_season
        #
        normalized_home_proporion = ((global_avg * (game_list.games_df["MaxGamesPerSeason"] -
                                                    game_list.games_df["HomeTeamGamesPlayedInSeason"])) +
                                     scoring_avg_home_team) / game_list.games_df["MaxGamesPerSeason"]
        normalized_away_proporion = ((global_avg * (game_list.games_df["MaxGamesPerSeason"] -
                                                    game_list.games_df["AwayTeamGamesPlayedInSeason"])) +
                                     scoring_avg_away_team) / (game_list.games_df["MaxGamesPerSeason"])

        # 3. The final score would be the average of home and away teams proportion
        game_list.games_df["LowScoringTeamsGenerator"] = (normalized_home_proporion + normalized_away_proporion) / 2

        return game_list

    def get_feature_names(self):
        return ["LowScoringTeamsGenerator"]
