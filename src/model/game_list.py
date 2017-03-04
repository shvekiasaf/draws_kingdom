class GameList:
    """Represents a list of games"""

    def __init__(self, list_name, games_df=None):
        self.games_df = games_df
        self.list_name = list_name
