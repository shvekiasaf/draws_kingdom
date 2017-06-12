from feature_generators.general_generator import GeneralGenerator


class DrawsPercentageGenerator(GeneralGenerator):

    def calculate_feature(self, game_list):

        if game_list is None:
            return game_list
        elif game_list.games_df is None:
            return game_list
        elif game_list.games_df.empty:
            return game_list

        teams_draw_percentage_dict = {}

        for index, game in game_list.games_df.iterrows():
            if game["HomeTeam"] not in teams_draw_percentage_dict:
                teams_draw_percentage_dict[game["HomeTeam"]] = {'draws': 0, 'total_games': 0}

            if game["AwayTeam"] not in teams_draw_percentage_dict:
                teams_draw_percentage_dict[game["AwayTeam"]] = {'draws': 0, 'total_games': 0}

            if game["Draw"]:
                teams_draw_percentage_dict[game["HomeTeam"]]['draws'] += 1
                teams_draw_percentage_dict[game["AwayTeam"]]['draws'] += 1

            teams_draw_percentage_dict[game["HomeTeam"]]['total_games'] += 1
            teams_draw_percentage_dict[game["AwayTeam"]]['total_games'] += 1

        for index, game in game_list.games_df.iterrows():
            home_team_data = teams_draw_percentage_dict[game["HomeTeam"]]
            away_team_data = teams_draw_percentage_dict[game["AwayTeam"]]
            game_list.games_df.loc[int(game.name), "DrawPercentage"] = ((away_team_data['draws'] / away_team_data['total_games']) + (home_team_data['draws'] / home_team_data['total_games'])) / 2

        return game_list
