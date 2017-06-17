import pandas as pd

from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from src.feature_generators.goals_difference_generator import GoalsDifferenceGenerator
from src.model.game_list import GameList


class TestGoalsDifferenceGenerator(BaseTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_game_mamy_games(self):
        BaseTestCase.clean_cache_files(self, ".*many_games.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games.csv",
                                                        league_name="tests")
        goals_difference = GoalsDifferenceGenerator().calculate_feature(game_list)
        self.assertEqual(goals_difference.games_df.loc[3, "ScoringDistance"], 0)
        self.assertEqual(goals_difference.games_df.loc[2, "ScoringDistance"], 2)

