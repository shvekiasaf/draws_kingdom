from feature_generators.distance_from_top_generator import DistanceFromTopGenerator
from feature_generators.points_difference_generator import PointsDifferenceGenerator
from helpers.url_helper import URLHelper
from predictors.prediction_manager import PredictionManager
from readers.reader_manager import ReaderManager
from feature_generators.draws_percentage_generator import DrawsPercentageGenerator
from feature_generators.league_points_generator import LeaguePointsGenerator
from feature_generators.goals_difference_generator import GoalsDifferenceGenerator
from feature_generators.league_goals_difference_normalized_generator import LeagueGoalsDifferenceNormalizedGenerator
from feature_generators.league_goals_avg_normalized_generator import LeagueGoalsAvgNormalizedGenerator

# if not game_list:
game_list = ReaderManager.all_game_lists(csv_file_names=["english_urls", "belgium_urls"],
                                         base_csv_folder_url=URLHelper.base_project_url() + "/readers/urls/")

print("- Feature Engineering")
LeaguePointsGenerator().calculate_feature(game_list)
PointsDifferenceGenerator().calculate_feature(game_list)
DistanceFromTopGenerator().calculate_feature(game_list)
GoalsDifferenceGenerator(365).calculate_feature(game_list)
GoalsDifferenceGenerator().calculate_feature(game_list)
DrawsPercentageGenerator(365).calculate_feature(game_list)
DrawsPercentageGenerator().calculate_feature(game_list)
LeagueGoalsDifferenceNormalizedGenerator().calculate_feature(game_list)
LeagueGoalsAvgNormalizedGenerator().calculate_feature(game_list)

print("- Running Predictions")
PredictionManager.run_prediction(game_list=game_list)

