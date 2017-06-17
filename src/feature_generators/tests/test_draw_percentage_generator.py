import pandas as pd

from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from src.feature_generators.draws_percentage_generator import DrawsPercentageGenerator
from src.feature_generators.league_points_generator import LeaguePointsGenerator
from src.model.game_list import GameList


class TestDrawPercentageGenerator(BaseTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_game_mamy_games(self):
        BaseTestCase.clean_cache_files(self, ".*many_games.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games.csv",
                                                        league_name="tests")
        draw_percentage = DrawsPercentageGenerator().calculate_feature(game_list)
        self.assertEqual(draw_percentage.games_df.loc[3, "DrawPercentage"], 0.5)

