from abc import ABC, abstractmethod


class BaseMetricPopulator(ABC):
    @abstractmethod
    def update_metric(self,game_list, max_points, number_of_games_played, row, season_id_team_points_dic):
        pass


def get_team_key(row, team):
    return row[team] + row["SeasonId"]