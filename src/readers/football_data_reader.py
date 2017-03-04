from model.team import Team
from model.game import Game
from model.game_list import GameList
from datetime import datetime
import csv
import urllib.request
import pickle
import os


class FootballDataReader:
    """An object that reads csv data from Football-Data.uk website, stores it in a cache
       file and returns a list of game list"""

    BASE_CACHE_URL = "readers/cache/"

    @staticmethod
    def game_list_by_url(url, league_name):

        def create_cache_folder_if_needed(folder_path):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        def read_game_list_from_disk(file_path):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as input:
                    tmp_cached_game_list = pickle.load(input)
                    return tmp_cached_game_list

        def read_game_list_from_csv(url, list_name):
            game_list = GameList(list_name)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = response.read().decode('utf-8').splitlines()

            reader = csv.DictReader(data)

            for row in reader:

                if row['HomeTeam'] and row['AwayTeam'] and row['FTHG'] \
                        and row['FTAG'] and row['Div'] and row['Date'] and season:
                    current_home_team = Team(row['HomeTeam'])
                    current_away_team = Team(row['AwayTeam'])
                    current_game = Game(current_home_team, current_away_team,
                                        int(row['FTHG']), int(row['FTAG']), row['Div'],
                                        datetime.strptime(row['Date'], '%d/%m/%y'), season, league_name)
                    game_list.append_game(current_game)

            return game_list

        def save_game_list_to_disk(file_path, game_list):
            # save list to disk
            with open(file_path, 'wb') as output:
                pickle.dump(game_list, output, pickle.HIGHEST_PROTOCOL)

        # list name will be the division name extracted out of the file
        list_name = url.split('/')[-1].split('.')[0]

        # extracting season from url
        season = url.split('/')[-2]

        # define cache folder and file paths
        cache_folder_path = FootballDataReader.BASE_CACHE_URL + "/" + league_name
        cache_file_path = cache_folder_path + "/" + list_name + season

        create_cache_folder_if_needed(cache_folder_path)
        cached_game_list = read_game_list_from_disk(cache_file_path)

        if cached_game_list:  # if cache existed
            return cached_game_list
        else:
            game_list = read_game_list_from_csv(url, list_name)
            save_game_list_to_disk(cache_file_path, game_list)
            return game_list
