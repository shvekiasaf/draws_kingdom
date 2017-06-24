from abc import ABC, abstractmethod
from helpers.file_helper import FileHelper
import datetime

from helpers.url_helper import URLHelper


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

    def calculate_feature(self, game_list, ignore_cache=False):

        feature_cache_path = URLHelper.cache_folder_path() + "features/" + self.get_printable_name() + ".dat"
        cached_game_list = FileHelper.read_object_from_disk(file_path=feature_cache_path)

        if cached_game_list is not None and not ignore_cache:
            game_list.games_df[self.get_feature_names()] = cached_game_list
            print('Feature ' + self.get_printable_name() + ' loaded from cache')
        else:
            if game_list is None:
                return game_list
            elif game_list.games_df is None:
                return game_list
            elif game_list.games_df.empty:
                return game_list
            start_time = datetime.datetime.now()
            game_list = self.inner_calculate_feature(game_list)
            end_time = datetime.datetime.now()
            print('Feature ' + self.get_printable_name() + ' took ' +
                  str((end_time - start_time).total_seconds()) + ' seconds')

            if not ignore_cache:
                FileHelper.save_object_to_disk(game_list.games_df[self.get_feature_names()], feature_cache_path)

        return game_list

    def get_printable_name(self):
        prefix = self.__class__.__name__
        if self.period:
            prefix = prefix + 'Period'
        return prefix

    def get_feature_names(self):
        pass
