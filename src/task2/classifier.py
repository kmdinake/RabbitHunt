import sys
from itertools import cycle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


__author__ = "Keoagile Dinake"
"""
Todo:
    This class serves as a data classifier agent that will do the following:
    1. preprocess data
    2. build a model
    3. classify data samples
    The user will be prompted on how to deal with the above mentioned
Author:
    Keoagile Dinake 14/11/2017
"""

RED = "\033[1;31m"
RESET = "\033[0;0m"
CYAN = "\033[1;36m"
LIME = "\033[0;32m"
ORANGE = "\033[0;35m"


class Classifier:
    def __init__(self):
        self.__nn = None
        self.__src_df = None
        self.__X_train = None
        self.__y_train = None
        self.__X_test = None
        self.__y_test = None

    def use_dataset(self, dataset_name):
        """
                Todo:
                    Read in a .csv file into a pandas datafame
                Params:
                    dataset_name -> Type: String
                Returns:
                    Void
                """
        if dataset_name is None or dataset_name == "":
            print(RED + "Dataset name cannot be null." + RESET)
            sys.exit(1)
        try:
            self.__src_df = pd.read_csv(dataset_name)
            print("Successfully read file: " + dataset_name)
        except IOError:
            print(RED + "Failed to locate and read from file: " + dataset_name + RESET)

    def prepare_dataset(self):
        # Normalize the Amount feature because it's overwhelming the other features
        scaler = StandardScaler()
        self.__src_df["Amount"] = scaler.fit_transform(self.__src_df["Amount"].values.reshape(-1, 1))
        self.__src_df = self.__src_df.drop(['Time'], axis=1)
        X = self.__src_df.loc[:, self.__src_df.columns != "Class"]
        y = self.__src_df.loc[:, self.__src_df.columns == "Class"]
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(
            X, y, test_size=0.33, random_state=0)
        # The MultiLayer Perceptron is sensitive to feature scaling so standardize our data
        scaler.fit(self.__X_train)  # scale only on training data to avoid over-fitted results
        self.__X_train = scaler.transform(self.__X_train)
        self.__X_test = scaler.transform(self.__X_test)  # apply the same transformation to ensure meaningful results

    def fit(self):
        print(CYAN + "Training using {} samples".format(len(self.__X_train)) + RESET)
        self.__nn = MLPClassifier(solver="adam", alpha=1e-5, random_state=1)
        self.__nn.fit(self.__X_train, self.__y_train.values.ravel())
        score = self.__nn.score(self.__X_test, self.__y_test)
        print("After fitting the model has a score of: " + ORANGE + str(score) + RESET)

    def predict_and_report(self):
        print(CYAN + "Testing using {} samples".format(len(self.__X_test)) + RESET)
        y_prediction = self.__nn.predict(self.__X_test)
        recall_accuracy = recall_score(self.__y_test.values, y_prediction)
        print("The model's recall score is: " + ORANGE + str(recall_accuracy) + RESET)

        y_prediction_prob = self.__nn.predict_proba(self.__X_test)

        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        colors = cycle(
            ['navy', 'turquoise', 'darkorange', 'cornflowerblue', 'teal', 'red', 'yellow', 'green', 'blue', 'black'])

        plt.figure(figsize=(5, 5))

        j = 1
        for i, color in zip(thresholds, colors):
            y_test_predictions_prob = y_prediction_prob[:, 1] > i
            precision, recall, thresholds = precision_recall_curve(self.__y_test, y_test_predictions_prob)
            # Plot Precision-Recall curve
            plt.plot(recall, precision, color=color, label='Threshold: %s' % i)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.ylim([0.0, 1.05])
            plt.xlim([0.0, 1.0])
            plt.title('Precision-Recall')
            plt.legend(loc="lower left")
        plt.savefig('reports/precision_recall.png', bbox_inches='tight')
        # plt.show()