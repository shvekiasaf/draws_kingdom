from abc import ABC, abstractmethod
import datetime


class GeneralGenerator(ABC):
    """Represents an abstract class of feature generators"""

    def __init__(self, period=None, *args,
                 **kwargs):  # in args, kwargs, there will be all parameters you don't care, but needed for baseClass
        super(GeneralGenerator, self).__init__()
        self.period = period

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
        start_time = datetime.datetime.now()
        result = self.inner_calculate_feature(game_list)
        end_time = datetime.datetime.now()
        print('feature ' + self.get_feature_name() + ' took ' +
              str((end_time - start_time).total_seconds()) + ' seconds')
        return result

    def get_feature_name(self):
        prefix = self.__class__.__name__
        if self.period:
            prefix = prefix + 'Period'
        return prefix
