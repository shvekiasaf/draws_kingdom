import pandas as pd

from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from src.feature_generators.draws_percentage_generator import DrawsPercentageGenerator


class TestDrawPercentageGenerator(BaseTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_mamy_games(self):
        BaseTestCase.clean_cache_files(self, ".*draw_perce.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/draw_percentage.csv",
                                                        league_name="tests")
        draw_percentage = DrawsPercentageGenerator().calculate_feature(game_list)
        self.assertEqual(draw_percentage.games_df.loc[0, "DrawsPercentageGenerator"], -1)
        self.assertEqual(draw_percentage.games_df.loc[1, "DrawsPercentageGenerator"], 0)
        self.assertEqual(draw_percentage.games_df.loc[2, "DrawsPercentageGenerator"], 0)
        self.assertEqual(draw_percentage.games_df.loc[3, "DrawsPercentageGenerator"], 1 / 3)
        self.assertEqual(draw_percentage.games_df.loc[4, "DrawsPercentageGenerator"], 0.5)

    def test_calculate_mamy_games_with_period(self):
        BaseTestCase.clean_cache_files(self, ".*draw_perce.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/draw_percentage.csv",
                                                        league_name="tests")
        draw_percentage = DrawsPercentageGenerator(2).calculate_feature(game_list)
        self.assertEqual(draw_percentage.games_df.loc[0, "DrawsPercentageGeneratorPeriod"], -1)
        self.assertEqual(draw_percentage.games_df.loc[1, "DrawsPercentageGeneratorPeriod"], 0)
        self.assertEqual(draw_percentage.games_df.loc[2, "DrawsPercentageGeneratorPeriod"], 0)
        self.assertEqual(draw_percentage.games_df.loc[3, "DrawsPercentageGeneratorPeriod"], 0.5)
        self.assertEqual(draw_percentage.games_df.loc[4, "DrawsPercentageGeneratorPeriod"], 1)