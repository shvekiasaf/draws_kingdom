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
        features = ['LeaguePointsDiff',
                    'GoalsDifferenceGenerator',
                    'DrawsPercentageGenerator',
                    'GoalsDifferenceGeneratorPeriod',
                    'DrawsPercentageGeneratorPeriod',
                    'DistanceFromTop',
                    'LeagueGoalsDifferenceNormalizedGenerator',
                    'LeagueGoalsAvgNormalizedGenerator'
                    ]
        data_frame = data_frame[features + ['Draw']]

        data_frame["Draw"] = data_frame["Draw"].astype("int")

        print("\nSplitting test=20% train=80%")
        train, test = train_test_split(data_frame, test_size=0.2, random_state=0)

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
        print("Draw: %i (%.1f percent), None Draw: %i (%.1f percent), Total: %i\n" \
              % (len(draw_test), 1. * len(draw_test) / len(test) * 100.0, \
                 len(non_draw_test), 1. * len(non_draw_test) / len(test) * 100.0, len(test)))
        baseline = 1. * len(draw_test) / len(test) * 100.0

        # Modelling
        tcols = np.append(['Draw'], features)

        df = train.loc[:, tcols].dropna()
        X = df.loc[:, features]
        y = np.ravel(df.loc[:, ['Draw']])

        df_test = test.loc[:, tcols].dropna()
        X_test = df_test.loc[:, features]
        y_test = np.ravel(df_test.loc[:, ['Draw']])

        # Logistic Regression:
        clf_log = LogisticRegression()
        PredictionManager.run_model(clf_log, "Logistic Regression", X, y, X_test, y_test, baseline)

        # Decision Tree:
        clf_tree = tree.DecisionTreeClassifier(
            # max_depth=3,\
            class_weight="balanced", \
            min_weight_fraction_leaf=0.01 \
            )
        clf_tree = clf_tree.fit(X, y)
        PredictionManager.run_model(clf_tree, "Decision Tree", X, y, X_test, y_test, baseline)

        # Extra Trees
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
        PredictionManager.run_model(clf_ext, "Extra Tree", X, y, X_test, y_test, baseline)

        # Random Forest:
        clf_rf = RandomForestClassifier(
            n_estimators=1000, \
            max_depth=None, \
            min_samples_split=10 \
            # class_weight="balanced", \
            # min_weight_fraction_leaf=0.02 \
        )
        clf_rf = clf_rf.fit(X, y)
        PredictionManager.run_model(clf_rf, "Random Forest", X, y, X_test, y_test, baseline)

        # clf = clf_ext
        # scores = cross_val_score(clf, X, y, cv=5)
        # print(scores)
        # print("Mean score = %.3f, Std deviation = %.3f" % (np.mean(scores), np.std(scores)))

        pass

    @staticmethod
    def run_model(model: object, modeltitle, X, y, X_test, y_test, baseline):
        clf = model.fit(X, y)

        model_score = cross_val_score(clf, X, y, cv=5).mean()
        print(Fore.BLUE)
        print(modeltitle)
        print(Style.RESET_ALL)
        print(" Score: ", model_score)

        conf_mat_ext = confusion_matrix(clf.predict(X_test), y_test, labels=[0, 1])

        draw_score = 100 * conf_mat_ext[1, 1] / (conf_mat_ext[1, 0] + conf_mat_ext[1, 1])

        print(conf_mat_ext)

        print(Fore.RED)
        if draw_score > baseline:
            print(Fore.GREEN)

        print("Draw score: %.5f (Baseline: %.5f)" % (draw_score, baseline))

        print(Style.RESET_ALL)
        print("\n")


# Code example how to engineer a feature:
# =======================================
# print("\nLeaguePointsDiff engineering")
# warnings.filterwarnings(action="ignore")
# plt.figure(figsize=[12, 10])
# plt.subplot(331)
# sns.distplot(draw['LeaguePointsDiff'].dropna().values, bins=range(0, 81, 1), kde=False, color="blue")
# sns.distplot(non_draw['LeaguePointsDiff'].dropna().values, bins=range(0, 81, 1), kde=False, color="red",
#              axlabel='LeaguePointsDiff')
# plt.subplot(332)
# print("Median league points draw: %.1f, Median league points none-draw: %.1f" \
#      % (np.median(draw['LeaguePointsDiff'].dropna()), np.median(non_draw['LeaguePointsDiff'].dropna())))
