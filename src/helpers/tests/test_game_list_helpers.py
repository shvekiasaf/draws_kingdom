import unittest
from helpers.game_list_helpers import split_games_to_seasons
from helpers.game_list_helpers import all_team_names_from_list
from model.game_list import GameList
from model.game import Game
from model.team import Team


class TestGameListHelpers(unittest.TestCase):
    def setUp(self):
        pass

    """split_games_to_seasons tests
    =================================="""
    def test_split_games_to_seasons__none_games(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=None)

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_split_games_to_seasons__none_game_list(self):

        # Arrange
        game_list = None

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_split_games_to_seasons__empty_game_list(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=[])

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_split_games_to_seasons__single_game(self):

        # Arrange
        game_1 = Game(league_name="L1", season="S1", division="D1")
        game_list = GameList(list_name="", list_of_games=[game_1])

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_games))
        self.assertEqual(all_games["L1S1D1"].games[0], game_1)

    def test_split_games_to_seasons__different_season_games(self):

        # Arrange
        game_1 = Game(league_name="L1", season="S1", division="D1")
        game_2 = Game(league_name="L1", season="S2", division="D1")
        game_list = GameList(list_name="", list_of_games=[game_1, game_2])

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_games))
        self.assertEqual(all_games["L1S1D1"].games[0], game_1)
        self.assertEqual(all_games["L1S2D1"].games[0], game_2)

    def test_split_games_to_seasons__many_games_per_season(self):

        # Arrange
        game_1 = Game(league_name="L1", season="S1", division="D1")
        game_2 = Game(league_name="L1", season="S1", division="D1")
        game_list = GameList(list_name="", list_of_games=[game_1, game_2])

        # Act
        all_games = split_games_to_seasons(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_games))
        self.assertEqual(len(all_games["L1S1D1"].games), 2)

    """all_team_names_from_list tests
        =========================="""
    def test_all_team_names_from_list__none_games(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=None)

        # Act
        all_games = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_all_team_names_from_list__none_game_list(self):

        # Arrange
        game_list = None

        # Act
        all_games = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_all_team_names_from_list__empty_game_list(self):

        # Arrange
        game_list = GameList(list_name="", list_of_games=[])

        # Act
        all_games = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertFalse(bool(all_games))

    def test_all_team_names_from_list__single_game(self):

        # Arrange
        team_1 = Team(team_name="team_1")
        team_2 = Team(team_name="team_2")
        game_1 = Game(home_team=team_1, away_team=team_2)
        game_list = GameList(list_name="", list_of_games=[game_1])

        # Act
        all_names = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_names))
        self.assertEqual(len(all_names), 2)
        self.assertEqual(sorted(all_names), sorted([team_1.name, team_2.name]))

    def test_all_team_names_from_list__single_game_same_teams(self):

        # Arrange
        team_1 = Team(team_name="team_1")
        game_1 = Game(home_team=team_1, away_team=team_1)
        game_list = GameList(list_name="", list_of_games=[game_1])

        # Act
        all_names = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_names))
        self.assertEqual(len(all_names), 1)
        self.assertEqual(all_names, [team_1.name])

    def test_all_team_names_from_list__many_games_identical_teams(self):

        # Arrange
        team_1 = Team(team_name="team_1")
        team_2 = Team(team_name="team_2")
        game_1 = Game(home_team=team_1, away_team=team_2)
        game_2 = Game(home_team=team_2, away_team=team_1)
        game_list = GameList(list_name="", list_of_games=[game_1, game_2])

        # Act
        all_names = all_team_names_from_list(game_list=game_list)

        # Assert
        self.assertTrue(bool(all_names))
        self.assertEqual(len(all_names), 2)
        self.assertEqual(sorted(all_names), sorted([team_1.name, team_2.name]))

    def tearDown(self):
        pass
