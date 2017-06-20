from helpers.file_helper import FileHelper
from helpers.url_helper import URLHelper
from predictors.prediction_manager import PredictionManager
from readers.reader_manager import ReaderManager
from feature_generators.draws_percentage_generator import DrawsPercentageGenerator
from feature_generators.league_points_generator import LeaguePointsGenerator
from feature_generators.goals_difference_generator import GoalsDifferenceGenerator
import datetime
game_list = FileHelper.read_object_from_disk(file_path=URLHelper.cache_folder_path() + "final_games.dat")

if not game_list:
    game_list = ReaderManager.all_game_lists(csv_file_names=["english_urls", "belgium_urls"],
                                             base_csv_folder_url=URLHelper.base_project_url() + "/readers/urls/")

    print("- Feature Engineering")
    GoalsDifferenceGenerator(365).calculate_feature(game_list)
    GoalsDifferenceGenerator().calculate_feature(game_list)
    league_points_generator = LeaguePointsGenerator()
    league_points_generator.calculate_feature(game_list)
    DrawsPercentageGenerator(365).calculate_feature(game_list)
    DrawsPercentageGenerator().calculate_feature(game_list)
    FileHelper.save_object_to_disk(game_list, file_path=URLHelper.cache_folder_path() + "final_games.dat")
else:
    print("- Using Cache")

print("- Running Predictions")
PredictionManager.run_prediction(game_list=game_list)

