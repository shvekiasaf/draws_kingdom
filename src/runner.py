from readers.reader_manager import ReaderManager
from feature_generators.league_points_generator import LeaguePointsGenerator

lists = ReaderManager.all_game_lists(["english_urls", "belgium_urls"], "readers/urls/")
# lists = ReaderManager.all_game_lists(["belgium_urls"], "readers/urls/")

ttt = LeaguePointsGenerator()
ttt.calculate_feature(lists)

pass
