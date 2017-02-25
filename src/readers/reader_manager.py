from model.game_list import GameList
from readers.football_data_reader import FootballDataReader

class ReaderManager:
    """Reads all data from all CSV files and manage cache"""

    BASE_CSVS_URL = "readers/urls/"

    @staticmethod
    def all_game_lists(files):

        all_games = GameList("All Games")
        for current_league_name in files:

            print("\n\nLoading CSVs for league: " + current_league_name)

            f = open(ReaderManager.BASE_CSVS_URL + current_league_name, 'r')

            for line in f:
                print(line, end='')

                temp_list = FootballDataReader.game_list_by_url(line, current_league_name)
                all_games.append_list(temp_list)

        return all_games
