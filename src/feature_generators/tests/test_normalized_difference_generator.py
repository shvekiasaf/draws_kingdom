from helpers.base_test_case import BaseTestCase
from readers.football_data_reader import FootballDataReader
from feature_generators.league_goals_difference_normalized_generator import LeagueGoalsDifferenceNormalizedGenerator
import pandas


class TestNormalizedDifferenceGenerator(BaseTestCase):
    def setUp(self):
        self.clean_cache_files(folder='e0_tests', pattern='.*-1[0-9]{1}.dat')

    def tearDown(self):
        pass

    def test_empty_df(self):
        no_games = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/E0-14.csv", league_name="e0_tests")
        no_games.games_df = pandas.DataFrame(columns=no_games.games_df.columns)
        LeagueGoalsDifferenceNormalizedGenerator().calculate_feature(no_games)

    def test_single_league_single_season(self):
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/E0-14.csv", league_name="e0_tests")
        result = LeagueGoalsDifferenceNormalizedGenerator().calculate_feature(game_list, ignore_cache=True)
        self.assertEqual(round(result.games_df.loc[0, "LeagueGoalsDifferenceNormalizedGenerator"], 2), 0.38)
        self.assertEqual(round(result.games_df.loc[169, "LeagueGoalsDifferenceNormalizedGenerator"], 3), 0.377)

    def test_multiple_leagues_multiple_seasons(self):
        game_list = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/E0-14.csv", league_name="e0_tests", season='E0-14')
        other_league = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/B1-14.csv", league_name="e0_tests", season='B1-14')
        second_season = FootballDataReader.game_list_by_url(url=BaseTestCase.base_url() + "/E0-15.csv", league_name="e0_tests", season='E0-15')
        game_list.games_df = pandas.concat([game_list.games_df, second_season.games_df, other_league.games_df],ignore_index=True)
        result = LeagueGoalsDifferenceNormalizedGenerator().calculate_feature(game_list, ignore_cache=True)
        self.assertEqual(round(result.games_df.loc[0, "LeagueGoalsDifferenceNormalizedGenerator"], 2), 0.38)
        self.assertEqual(round(result.games_df.loc[169, "LeagueGoalsDifferenceNormalizedGenerator"], 3), 0.377)


