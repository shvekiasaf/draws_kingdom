from model.game_list import GameList
from readers.football_data_reader import FootballDataReader
import pandas as pd


class ReaderManager:
    """Reads all data from all CSV files"""

    @staticmethod
    def all_game_lists(csv_file_names, base_csv_folder_url):

        all_games = GameList("All Games", pd.DataFrame())
        for current_league_name in csv_file_names:

            print("- Loading CSVs for league: " + current_league_name)

            f = open(base_csv_folder_url + current_league_name, 'r')

            for line in f:
                print(line, end='')

                temp_game_list = FootballDataReader.game_list_by_url(url=line, league_name=current_league_name)

                if all_games.games_df.empty:
                    all_games.games_df = temp_game_list.games_df
                else:
                    all_games.games_df = pd.concat([temp_game_list.games_df, all_games.games_df], ignore_index=True)

            print("\n")

        return all_games
