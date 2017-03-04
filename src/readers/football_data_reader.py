from model.game_list import GameList
import pickle
import os
import pandas as pd


class FootballDataReader:
    """An object that reads csv data from Football-Data.uk website, stores it in a cache
       file and returns a list of game list"""

    BASE_CACHE_URL = "readers/cache/"

    @staticmethod
    def game_list_by_url(url, league_name, season=""):

        def create_cache_folder_if_needed(folder_path):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        def read_game_list_from_disk(file_path):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as input:
                    tmp_cached_game_list = pickle.load(input)
                    return tmp_cached_game_list

        def read_game_list_from_csv(url, list_name, season, league_name):

            data_frame = pd.read_csv(url, usecols=["HomeTeam", "AwayTeam", "Div", "Date", "FTAG", "FTHG"])
            data_frame["LeagueName"] = league_name  # new feature
            data_frame["Season"] = season  # new feature
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

            current_game_list = GameList(list_name, data_frame)

            return current_game_list

        def save_game_list_to_disk(file_path, game_list):
            # save list to disk
            with open(file_path, 'wb') as output:
                pickle.dump(game_list, output, pickle.HIGHEST_PROTOCOL)

        base_project_path = os.path.abspath("s").split("src")[0] + "src/"

        # list name will be the division name extracted out of the file
        list_name = url.split('/')[-1].split('.')[0]

        # extracting season from url
        if not season:
            season = url.split('/')[-2]

        # define cache folder and file paths
        cache_folder_path = base_project_path + FootballDataReader.BASE_CACHE_URL + league_name
        cache_file_path = cache_folder_path + "/" + list_name + season

        create_cache_folder_if_needed(cache_folder_path)
        cached_game_list = read_game_list_from_disk(cache_file_path)

        if cached_game_list:  # if cache existed
            return cached_game_list
        else:
            game_list = read_game_list_from_csv(url, list_name, season, league_name)
            save_game_list_to_disk(cache_file_path, game_list)
            return game_list
