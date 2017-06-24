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

    def test_calculate_mamy_games(self):
        BaseTestCase.clean_cache_files(self, ".*.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/goals_difference.csv",
                                                        league_name="tests")
        goals_difference = GoalsDifferenceGenerator().calculate_feature(game_list, ignore_cache=True)
        self.assertEqual(goals_difference.games_df.loc[2, "GoalsDifferenceGenerator"], 1)
        self.assertEqual(goals_difference.games_df.loc[3, "GoalsDifferenceGenerator"], 0)
        self.assertEqual(goals_difference.games_df.loc[4, "GoalsDifferenceGenerator"], 2)

    def test_calculate_mamy_games_with_period(self):
        BaseTestCase.clean_cache_files(self, ".*.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/goals_difference.csv",
                                                        league_name="tests")
        goals_difference = GoalsDifferenceGenerator(2).calculate_feature(game_list, ignore_cache=True)
        self.assertEqual(goals_difference.games_df.loc[2, "GoalsDifferenceGeneratorPeriod"], 1)
        self.assertEqual(goals_difference.games_df.loc[3, "GoalsDifferenceGeneratorPeriod"], 0)
        self.assertEqual(goals_difference.games_df.loc[4, "GoalsDifferenceGeneratorPeriod"], 0)

