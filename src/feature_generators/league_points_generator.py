from feature_generators.general_generator import GeneralGenerator
from helpers.game_list_helpers import *


class LeaguePointsGenerator(GeneralGenerator):
    """A generator that adds the current league points for every team in a game.
    Affected game attributes: home_team_league_points and away_team_league_points"""

    def calculate_feature(self, game_list):

        seasons_dict = split_games_to_seasons(game_list)

        for current_season in seasons_dict:

            all_teams = all_team_names_from_list(seasons_dict[current_season])
            all_teams_points_dic = {x: 0 for x in all_teams}

            for current_game in seasons_dict[current_season].games:

                # first, add the current number of points to the team
                current_game.home_team_league_points = all_teams_points_dic[current_game.home_team.name]
                current_game.away_team_league_points = all_teams_points_dic[current_game.away_team.name]

                # then, calculate the new teams points
                if current_game.home_score > current_game.away_score:
                    all_teams_points_dic[current_game.home_team.name] += 3
                elif current_game.home_score == current_game.away_score:
                    all_teams_points_dic[current_game.home_team.name] += 1
                    all_teams_points_dic[current_game.away_team.name] += 1
                else:
                    all_teams_points_dic[current_game.away_team.name] += 3

                print(current_season + "\n")
                print("{" + "\n".join("{}: {}".format(k, v) for k, v in all_teams_points_dic.items()) + "}")
                print("\n")

        return game_list