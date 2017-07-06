from feature_generators.league_points_generator import LeaguePointsGenerator
from feature_generators.low_scoring_teams_generator import LowScoringTeamsGenerator
from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader


class TestLowScoringTeamsGenerator(BaseTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_feature__many_games_one_season(self):

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games_low_scoring.csv",
                                                        league_name="many_games")

        LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Act
        LowScoringTeamsGenerator().calculate_feature(game_list, ignore_cache=True)

        # Assert
        self.assertEqual(game_list.games_df.loc[0, "LowScoringTeamsGenerator"], (1+1/3))
        self.assertEqual(game_list.games_df.loc[5, "LowScoringTeamsGenerator"],
                         (((1+1/3)*1+3.5)/3 + ((1+1/3)*1+0.5)/3)/2)
