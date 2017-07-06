import pandas as pd

from feature_generators.distance_from_top_generator import DistanceFromTopGenerator
from feature_generators.points_difference_generator import PointsDifferenceGenerator
from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from src.feature_generators.league_points_generator import LeaguePointsGenerator
from src.model.game_list import GameList


class TestLeaguePointsGenerator(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_feature__no_data_frame(self):
        # Arrange
        game_list = GameList(list_name="", games_df=None)

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertFalse(bool(game_list_with_points.games_df))

    def test_calculate_feature__none_game_list(self):
        # Arrange
        game_list = None

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertFalse(bool(game_list_with_points))

    def test_calculate_feature__empty_data_frame(self):
        # Arrange
        game_list = GameList(list_name="", games_df=pd.DataFrame())

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertTrue(game_list_with_points.games_df.empty)

    def test_calculate_feature__single_game(self):
        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/single_game.csv",
                                                        league_name="tests")

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertTrue(bool(game_list_with_points))
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "MaxGamesPerSeason"], 1)

        self.assertEqual(len(game_list_with_points.games_df.index), 1)

    def test_calculate_feature__many_games(self):
        BaseTestCase.clean_cache_files(self, ".*many_games.*dat")

        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games.csv",
                                                        league_name="tests")

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)
        game_list_with_points = PointsDifferenceGenerator().calculate_feature(game_list=game_list_with_points, ignore_cache=True)
        game_list_with_points = DistanceFromTopGenerator().calculate_feature(game_list=game_list_with_points, ignore_cache=True)

        # Assert
        self.assertTrue(bool(game_list_with_points))
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamLeaguePoints"], 3)
        self.assertEqual(game_list_with_points.games_df.loc[2, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[2, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamLeaguePoints"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamLeaguePoints"], 1)

        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "MaxGamesPerSeason"], 3)

        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamGamesPlayedInSeason"], 1)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamGoalsScoredInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "MaxGamesPerSeason"], 3)

        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamGoalsScoredInSeason"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamGoalsScoredInSeason"], 4)
        self.assertEqual(game_list_with_points.games_df.loc[3, "MaxGamesPerSeason"], 3)

        self.assertEqual(len(game_list_with_points.games_df.index), 4)
        draws = [False, False, True, True]
        for index in range(len(draws)):
            self.assertEqual(draws[index], game_list_with_points.games_df["Draw"][index])

        # todo move to a different test class
        self.assertEqual(game_list_with_points.games_df.loc[3, "LeaguePointsDiff"], 5)
        self.assertEqual(game_list_with_points.games_df.loc[3, "DistanceFromTop"], 1.25)

    def test_calculate_feature__many_unsorted_games(self):
        # Arrange
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_unsorted_games.csv",
                                                        league_name="tests")

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertTrue(bool(game_list_with_points))
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamLeaguePoints"], 3)
        self.assertEqual(game_list_with_points.games_df.loc[2, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[2, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamLeaguePoints"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamLeaguePoints"], 1)

        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "MaxGamesPerSeason"], 3)

        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGoalsScoredInSeason"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGoalsScoredInSeason"], 4)
        self.assertEqual(game_list_with_points.games_df.loc[0, "MaxGamesPerSeason"], 3)

        self.assertEqual(len(game_list_with_points.games_df.index), 4)

    def test_calculate_feature__many_games_different_seasons(self):
        BaseTestCase.clean_cache_files(self, ".*many_games.*dat")

        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games.csv",
                                                        league_name="tests", season="0910")
        game_list1 = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/many_games.csv",
                                                         league_name="tests", season="1011")

        game_list.games_df = pd.concat([game_list.games_df, game_list1.games_df], ignore_index=True)

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list, ignore_cache=True)

        # Assert
        self.assertTrue(bool(game_list_with_points))
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[1, "HomeTeamLeaguePoints"], 3)
        self.assertEqual(game_list_with_points.games_df.loc[2, "AwayTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[2, "HomeTeamLeaguePoints"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamLeaguePoints"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamLeaguePoints"], 1)
        self.assertEqual(game_list_with_points.games_df.loc[7, "AwayTeamLeaguePoints"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[7, "HomeTeamLeaguePoints"], 1)
        self.assertEqual(len(game_list_with_points.games_df.index), 8)

        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGamesPlayedInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "HomeTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "AwayTeamGoalsScoredInSeason"], 0)
        self.assertEqual(game_list_with_points.games_df.loc[0, "MaxGamesPerSeason"], 3)

        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[3, "HomeTeamGoalsScoredInSeason"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[3, "AwayTeamGoalsScoredInSeason"], 4)
        self.assertEqual(game_list_with_points.games_df.loc[3, "MaxGamesPerSeason"], 3)

        self.assertEqual(game_list_with_points.games_df.loc[7, "HomeTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[7, "AwayTeamGamesPlayedInSeason"], 2)
        self.assertEqual(game_list_with_points.games_df.loc[7, "HomeTeamGoalsScoredInSeason"], 6)
        self.assertEqual(game_list_with_points.games_df.loc[7, "AwayTeamGoalsScoredInSeason"], 4)
        self.assertEqual(game_list_with_points.games_df.loc[7, "MaxGamesPerSeason"], 3)
