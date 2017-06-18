import pandas as pd

from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from src.feature_generators.draws_percentage_generator import DrawsPercentageGenerator


class TestDrawPercentageGenerator(BaseTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_game_mamy_games(self):
        BaseTestCase.clean_cache_files(self, ".*draw_perce.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/draw_percentage.csv",
                                                        league_name="tests")
        draw_percentage = DrawsPercentageGenerator().calculate_feature(game_list)
        self.assertEqual(draw_percentage.games_df.loc[0, "DrawPercentage"], -1)
        self.assertEqual(draw_percentage.games_df.loc[1, "DrawPercentage"], 0)
        self.assertEqual(draw_percentage.games_df.loc[2, "DrawPercentage"], 0)
        self.assertEqual(draw_percentage.games_df.loc[3, "DrawPercentage"], 1 / 3)
        self.assertEqual(draw_percentage.games_df.loc[4, "DrawPercentage"], 0.5)