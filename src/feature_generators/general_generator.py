from abc import ABC, abstractmethod


class GeneralGenerator(ABC):
    """Represents an abstract class of feature generators"""

    @abstractmethod
    def calculate_feature(self, game_list):
        """gets a game list and calculate a specific game attribute
        for all games in the list"""
        pass
