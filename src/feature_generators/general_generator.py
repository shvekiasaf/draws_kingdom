from abc import ABC, abstractmethod


class GeneralGenerator(ABC):
    """Represents an abstract class of feature generators"""

    @abstractmethod
    def inner_calculate_feature(self, game_list):
        """gets a game list and calculate a specific game attribute
                for all games in the list"""
        pass

    def calculate_feature(self, game_list):
        if game_list is None:
            return game_list
        elif game_list.games_df is None:
            return game_list
        elif game_list.games_df.empty:
            return game_list
        return self.inner_calculate_feature(game_list)

    def filter_games_before_date(self, game_list, date):
        return game_list.games_df.loc[game_list.games_df['Date'] < date]