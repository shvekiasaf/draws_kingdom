import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier

from model.game_list import GameList
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.metrics import confusion_matrix
from colorama import Fore, Back, Style

class PredictionManager:
    """Manages the prediction workflow"""

    @staticmethod
    def run_prediction(game_list: GameList):
        data_frame = game_list.games_df

        # Feature selection
        data_frame = data_frame[['LeaguePointsDiff', 'Draw']]

        data_frame["Draw"] = data_frame["Draw"].astype("category")
        data_frame["Draw"].cat.categories = [0, 1]
        data_frame["Draw"] = data_frame["Draw"].astype("int")

        train, test = train_test_split(data_frame, test_size=0.2, random_state=0)

        train.head(8)

        train.describe()

        print('\nMissing Data Summary:')
        print(train.isnull().sum())

        draw = train[train['Draw'] == 1]
        non_draw = train[train['Draw'] == 0]

        print('\nTrain Data Summary:')
        print("Draw: %i (%.1f percent), None Draw: %i (%.1f percent), Total: %i" \
              % (len(draw), 1. * len(draw) / len(train) * 100.0, \
                 len(non_draw), 1. * len(non_draw) / len(train) * 100.0, len(train)))


        draw_test = test[test['Draw'] == 1]
        non_draw_test = test[test['Draw'] == 0]

        print('\nTest Data Summary:')
        print("Draw: %i (%.1f percent), None Draw: %i (%.1f percent), Total: %i" \
              % (len(draw_test), 1. * len(draw_test) / len(test) * 100.0, \
                 len(non_draw_test), 1. * len(non_draw_test) / len(test) * 100.0, len(test)))
        baseline = 1. * len(draw_test) / len(test) * 100.0

        print("\nLeaguePointsDiff engineering")
        # warnings.filterwarnings(action="ignore")
        # plt.figure(figsize=[12, 10])
        # plt.subplot(331)
        # sns.distplot(draw['LeaguePointsDiff'].dropna().values, bins=range(0, 81, 1), kde=False, color="blue")
        # sns.distplot(non_draw['LeaguePointsDiff'].dropna().values, bins=range(0, 81, 1), kde=False, color="red",
        #              axlabel='LeaguePointsDiff')
        # plt.subplot(332)

        print("Median league points draw: %.1f, Median league points none-draw: %.1f" \
              % (np.median(draw['LeaguePointsDiff'].dropna()), np.median(non_draw['LeaguePointsDiff'].dropna())))

        training, testing = train_test_split(train, test_size=0.2, random_state=0)
        print("\nTotal sample size = %i; training sample size = %i, testing sample size = %i" \
              % (train.shape[0], training.shape[0], testing.shape[0]))

        # Modelling
        cols = ['LeaguePointsDiff']
        tcols = np.append(['Draw'], cols)

        df = training.loc[:, tcols].dropna()
        X = df.loc[:, cols]
        y = np.ravel(df.loc[:, ['Draw']])

        df_test = testing.loc[:, tcols].dropna()
        X_test = df_test.loc[:, cols]
        y_test = np.ravel(df_test.loc[:, ['Draw']])

        # Logistic Regression:
        clf_log = LogisticRegression()
        PredictionManager.run_model(clf_log, "Logistic Regression", X, y, X_test, y_test, baseline)

        #Decision Tree:
        clf_tree = tree.DecisionTreeClassifier(
            # max_depth=3,\
            class_weight="balanced", \
            min_weight_fraction_leaf=0.01 \
            )
        clf_tree = clf_tree.fit(X, y)
        PredictionManager.run_model(clf_tree, "Decision Tree", X, y, X_test, y_test, baseline)

        clf_ext = ExtraTreesClassifier(
            max_features='auto',
            bootstrap=True,
            oob_score=True,
            n_estimators=1000,
            max_depth=None,
            min_samples_split=10
            # class_weight="balanced",
            # min_weight_fraction_leaf=0.02
        )
        clf_ext = clf_ext.fit(X, y)
        PredictionManager.run_model(clf_ext, "Extra Tree Score", X, y, X_test, y_test, baseline)

        # # Random Forest:
        # clf_rf = RandomForestClassifier(
        #     n_estimators=1000, \
        #     max_depth=None, \
        #     min_samples_split=10 \
        #     # class_weight="balanced", \
        #     # min_weight_fraction_leaf=0.02 \
        # )
        # clf_rf = clf_rf.fit(X, y)
        # score_rf = cross_val_score(clf_rf, X, y, cv=5).mean()
        # print("Random Forest Score: ", score_rf)
        # pd.DataFrame(list(zip(X.columns, np.transpose(clf_log.coef_))))
        # print(confusion_matrix(clf_rf.predict(X_test), y_test, labels=[0,1]))


        clf = clf_ext
        scores = cross_val_score(clf, X, y, cv=5)
        print(scores)
        print("Mean score = %.3f, Std deviation = %.3f" % (np.mean(scores), np.std(scores)))

        pass

    @staticmethod
    def run_model(model: object, modeltitle, X, y, X_test, y_test, baseline):
        clf = model.fit(X, y)

        model_score = cross_val_score(clf, X, y, cv=5).mean()
        print(modeltitle, " Score: ", model_score)

        conf_mat_ext = confusion_matrix(clf.predict(X_test), y_test, labels=[0, 1])

        draw_score = 100 * conf_mat_ext[1, 1] / (conf_mat_ext[1, 0] + conf_mat_ext[1, 1])

        print(conf_mat_ext)

        print(Fore.RED)
        if draw_score > baseline:
            print(Fore.GREEN)

        print("Draw score: %.5f (Baseline: %.5f)" % (draw_score, baseline))

        print(Style.RESET_ALL)
        print("\n")

