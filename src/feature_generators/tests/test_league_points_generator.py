import unittest
from src.feature_generators.league_points_generator import LeaguePointsGenerator
from src.model.game_list import GameList
from src.model.game import Game
from src.model.team import Team

class TestLeaguePointsGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_feature__none_games(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=None)

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list)

        # Assert
        self.assertFalse(bool(game_list_with_points.games))

    def test_calculate_feature__none_game_list(self):

        # Arrange
        game_list = None

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list)

        # Assert
        self.assertFalse(bool(game_list_with_points))

    def test_calculate_feature__empty_game_list(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=[])

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list)

        # Assert
        self.assertEqual(len(game_list_with_points.games), 0)

    def test_calculate_feature__single_game(self):

        # Arrange
        team_1 = Team(team_name="team_1")
        team_2 = Team(team_name="team_2")
        game_1 = Game(home_team=team_1, away_team=team_2, league_name="L1", season="S1", division="D1")
        game_list = GameList(list_name="", list_of_games=[game_1])

        # Act
        game_list_with_points = LeaguePointsGenerator().calculate_feature(game_list=game_list)

        # Assert
        self.assertTrue(bool(game_list_with_points))
        self.assertEqual(game_list_with_points.games[0].home_team_league_points, 0)
        self.assertEqual(game_list_with_points.games[0].away_team_league_points, 0)

    def test_calculate_feature__many_games(self):
        self.assertTrue(False)

    def test_calculate_feature__many_unsorted_games(self):
        self.assertTrue(False)

    def test_calculate_feature__many_games_different_seasons(self):
        self.assertTrue(False)
