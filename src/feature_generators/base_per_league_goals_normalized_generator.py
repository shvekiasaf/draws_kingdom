from abc import abstractmethod
from feature_generators.general_generator import GeneralGenerator
import pandas
import datetime


class BaseLeagueGoalsNormalizedGenerator(GeneralGenerator):
    def inner_calculate_feature(self, game_list):

        league_names = game_list.games_df['LeagueName'].unique()
        for league_name in league_names:
            league_df = game_list.games_df[game_list.games_df.LeagueName == league_name]
            self.handle_league(game_list, league_df)
        return game_list

    def handle_league(self, game_list, league_df):

        seasons = league_df.Season.unique()
        for season in seasons:
            season_df = league_df[league_df.Season == season]
            self.handle_season(game_list, season_df)

    def handle_season(self, game_list, season_df):
        if season_df.empty:
            return
        previous_games = pandas.DataFrame(columns=game_list.games_df.columns, dtype=float)
        a_team = season_df.HomeTeam.iloc[0]
        games_in_season = season_df[(season_df.HomeTeam == a_team) | (season_df.AwayTeam == a_team)].Div.count()
        season_average_score = self.get_game_grade(season_df.FTHG.mean(), season_df.FTAG.mean())
        for index, game in season_df.sort_values(by="Date").iterrows():

            if self.period:
                previous_games = previous_games[previous_games.Date >= game.Date - datetime.timedelta(days=self.period)]

            home_team_never_played_home = game.HomeTeam not in previous_games.HomeTeam.values
            away_team_never_played_away = game.AwayTeam not in previous_games.AwayTeam.values

            if previous_games.empty or (home_team_never_played_home and away_team_never_played_away):
                grade = 0
            else:
                if home_team_never_played_home:
                    # if home team never played at home, we take the average scoring against the away team when they
                    # play away
                    home_team_mean = previous_games.groupby('AwayTeam').mean()
                    team_for_home_team = 'AwayTeam'
                else:
                    home_team_mean = previous_games.groupby('HomeTeam').mean()
                    team_for_home_team = 'HomeTeam'

                if away_team_never_played_away:
                    # if away team never played away, we take the average scoring against the home team when they
                    # play at home
                    away_team_mean = previous_games.groupby('HomeTeam').mean()
                    team_for_away_team = 'HomeTeam'
                else:
                    away_team_mean = previous_games.groupby('AwayTeam').mean()
                    team_for_away_team = 'AwayTeam'
                grade = self.get_game_grade(home_team_mean['FTHG'][game[team_for_home_team]],
                                            away_team_mean['FTAG'][game[team_for_away_team]])
            if previous_games.empty:
                num_games_so_far = 0
            else:
                num_games_so_far = previous_games[(previous_games.HomeTeam == game.HomeTeam) | (previous_games.AwayTeam == game.HomeTeam)].Div.count()

            normalized_grade = (((
                                     (games_in_season - num_games_so_far) * season_average_score) + (grade * num_games_so_far))
                                / games_in_season)
            game_list.games_df.loc[(game_list.games_df.Date == game.Date) & (game_list.games_df.HomeTeam == game.HomeTeam), self.get_printable_name()] = normalized_grade
            previous_games = previous_games.append(game)

    def get_feature_names(self):
        return [self.get_printable_name()]

    @abstractmethod
    def get_game_grade(self, home_team_score, away_team_score):
        pass
