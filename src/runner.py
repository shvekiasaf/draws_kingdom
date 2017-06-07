from helpers.file_helper import FileHelper
from helpers.url_helper import URLHelper
from predictors.predictor_manager import PredictorManager
from readers.reader_manager import ReaderManager
from feature_generators.league_points_generator import LeaguePointsGenerator

game_list = FileHelper.read_object_from_disk(file_path=URLHelper.cache_folder_path() + "final_games.dat")

if not game_list:
    game_list = ReaderManager.all_game_lists(csv_file_names=["english_urls", "belgium_urls"],
                                             base_csv_folder_url=URLHelper.base_project_url() + "/readers/urls/")

    print("- Feature Engineering")
    ttt = LeaguePointsGenerator()
    ttt.calculate_feature(game_list)

    FileHelper.save_object_to_disk(game_list, file_path=URLHelper.cache_folder_path() + "final_games.dat")
else:
    print("- Using Cache")

print("- Running Predictions")
PredictorManager.run_prediction(game_list=game_list)

