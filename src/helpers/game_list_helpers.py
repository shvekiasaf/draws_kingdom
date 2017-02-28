from model.game_list import GameList


def split_games_to_seasons(game_list):
    """The function takes game list and split it to dictionary of seasons
    keys: season id
    values: game list of games for the specific season id"""

    games_dictionary = {}

    for current_game in game_list.games:
        if not current_game.seasonId in games_dictionary:
            games_dictionary[current_game.seasonId] = []
        games_dictionary[current_game.seasonId].append(current_game)

    for key in games_dictionary:
        games_dictionary[key] = GameList(key, games_dictionary[key])

    return games_dictionary


def all_teams_from_list(game_list):
    """Returns a unique team names list out of game list"""

    unique = []
    only_names = list(map((lambda x: x.home_team.name), game_list.games))
    [unique.append(item) for item in only_names if item not in unique]

    return unique
