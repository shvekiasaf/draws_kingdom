class GameList:
    """Represents a list of games"""

    def __init__(self, list_name, list_of_games=[]):
        self.games = list_of_games
        self.list_name = list_name

    def append_game(self, game):
        self.games.append(game)

    def append_list(self, game_list):
        self.games = self.games + game_list.games


