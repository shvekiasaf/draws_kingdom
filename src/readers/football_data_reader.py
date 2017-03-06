from helpers.file_helper import FileHelper
from helpers.url_helper import URLHelper
from model.game_list import GameList
import pandas as pd


class FootballDataReader:
    """An object that reads csv data from Football-Data.uk website, stores it in a cache
       file and returns a list of game list"""

    BASE_CACHE_URL = "readers/cache/"

    @staticmethod
    def game_list_by_url(url, league_name, season=""):

        def read_game_list_from_csv(_url, _division, _season, _league_name):

            data_frame = pd.read_csv(_url, usecols=["HomeTeam", "AwayTeam", "Div", "Date", "FTAG", "FTHG"])
            data_frame["LeagueName"] = _league_name  # new feature
            data_frame["Season"] = _season  # new feature
            data_frame["SeasonId"] = data_frame["LeagueName"] + \
                                     data_frame["Div"] + \
                                     data_frame["Season"]

            # Modeling
            data_frame["HomeTeam"] = data_frame["HomeTeam"].astype("category")
            data_frame["AwayTeam"] = data_frame["AwayTeam"].astype("category")
            data_frame["Div"] = data_frame["Div"].astype("category")
            data_frame["Season"] = data_frame["Season"].astype("category")
            data_frame["LeagueName"] = data_frame["LeagueName"].astype("category")
            data_frame["Date"] = pd.to_datetime(data_frame["Date"], format="%d/%m/%y")

            # setting the draw field
            data_frame.ix[data_frame.FTAG == data_frame.FTHG, "Draw"] = True
            data_frame.ix[data_frame.FTAG != data_frame.FTHG, "Draw"] = False

            current_game_list = GameList(_division, data_frame)

            return current_game_list

        # extracting the division from url
        division = url.split('/')[-1].split('.')[0]

        # extracting the season from url
        if not season:
            season = url.split('/')[-2]

        # define cache folder and file paths
        cache_folder_path = URLHelper.cache_folder_path() + league_name
        cache_file_path = cache_folder_path + "/" + division + season + ".dat"

        cached_game_list = FileHelper.read_object_from_disk(cache_file_path)

        if cached_game_list:  # if cache existed
            return cached_game_list
        else:
            game_list = read_game_list_from_csv(url, division, season, league_name)
            FileHelper.save_object_to_disk(game_list, cache_file_path)
            return game_list
