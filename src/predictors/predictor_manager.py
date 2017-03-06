from model.game_list import GameList
import matplotlib.pyplot as plt
import seaborn as sns

class PredictorManager:
    """Manage the prediction workflow"""

    @staticmethod
    def run_prediction(game_list: GameList):

        data_frame = game_list.games_df

        # Feature selection
        data_frame = data_frame[['LeaguePointsDiff', 'Draw']]

        colormap = plt.cm.viridis
        plt.figure(figsize=(2,2))
        plt.title('Pearson Correlation of Features', y=1.05, size=15)
        sns.heatmap(data_frame.astype(float).corr(),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)

