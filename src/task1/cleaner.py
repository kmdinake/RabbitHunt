import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


__author__ = "Keoagile Dinake"
"""
Todo:
    This class serves as a data cleaning agent that will do the following:
    1. find missing values
    2. find duplicate records
    3. find outliers
    The user will be prompted on how to deal with the above mentioned
Author:
    Keoagile Dinake 14/11/2017
"""

RED = "\033[1;31m"
RESET = "\033[0;0m"
CYAN = "\033[1;36m"
LIME = "\033[0;32m"
ORANGE = "\033[0;35m"


class Cleaner:
    def __init__(self):
        self.__src_df = None

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

    def scrub_dataset(self):
        """ 
        Todo:
            Essentially this method cleans the internal reference to the dataset.
        Params:
            No parameters
        Returns:
            Void
        """
        print(ORANGE + "Attempting to find duplicate records..." + RESET)
        self.__find_duplicate_records()
        print(ORANGE + "Attempting to find missing values..." + RESET)
        self.__find_missing_values()
        print(ORANGE + "Attempting to find outliers..." + RESET)
        self.__find_outliers()

    def plotify(self):
        print(ORANGE + "Plotting: The number of employees that leave per department" + RESET)
        self.__dept_plot()
        print(ORANGE + "Plotting: The number of employees that leave per salary average" + RESET)
        self.__salary_plot()
        print(ORANGE + "Plotting: Overworked and unrecognised employee position" + RESET)
        self.__project_hrs_promotion_plot()
        print(ORANGE + "Plotting: Overworked and undervalued employee position" + RESET)
        self.__project_hrs_salary_plot()
        print(ORANGE + "Plotting: Effect of work accident on employees" + RESET)
        self.__accident_plot()
        print(ORANGE + "Plotting: Effect of satisfaction level on employees" + RESET)
        self.__satisfaction_plot()
        print(ORANGE + "All plots are located in the reports folder." + RESET)

    """ Helper Methods """

    def __find_missing_values(self):
        """
        Todo:
            Find the missing values for each coloumn in the dataset.
            Ask the user whether, for all coloumns, to interporlate the median (nominal) or mode (categorical)
            to replace the missing values.
        Params:
            No parameters
        Returns:
            Void
        """
        answer = raw_input("Do you want to populate missing values with their respective median/mode values (y/n)? ")
        if answer == 'n':
            print("Skipping missing values")
            return
        else:
            medians = self.__src_df.median(axis=0).values
            modes = self.__src_df.mode(axis=0).values[0]
            col_count = len(self.__src_df.columns)
            missing_value_count = 0
            for ix in xrange(col_count):
                rec = self.__src_df.values[ix]
                for jx in range(len(rec)):
                    if rec[jx] in [None, "", np.inf, -np.inf, np.nan] or pd.isnull(rec[jx]):  # if missing value
                        missing_value_count += 1
                        if isinstance(modes[jx], str):
                            self.__src_df.values[ix][jx] = modes[jx]
                        else:
                            self.__src_df.values[ix][jx] = medians[jx]
            print(str(missing_value_count) + " missing values were found and successfully dealt with.")

    def __find_duplicate_records(self):
        """
        Todo:
            Find the duplicate records in the dataset.
            Ask the user if all duplicate records should be kept or removed from the dataset.
        Params:
            No parameters
        Returns:
            Void
        """
        temp = self.__src_df
        old_count = len(temp)
        temp = temp.drop_duplicates()
        new_count = len(temp)
        if new_count == old_count:
            print("No duplicate records found.")
            return
        answer = raw_input("Do you want to keep all duplicate records (y/n)? ")
        if answer == 'n':
            self.__src_df = temp
            count = old_count - new_count
            print("Successfully removed " + str(count) + " duplicate records.")
        else:
            print("Keeping duplicate records.")
            return

    def __find_outliers(self):
        """
        Todo:
            Find all outliers for each coloumn in the dataset.
            Ask the user if all records containing outliers should be replaced with the median value.
        Params:
            No parameters
        Returns:
            Void
        """
        rem_ans, rep_ans = "", ""
        rem_ans = raw_input(
            "If any outliers are found, do you want to remove all records containing these outliers(y/n)? ")
        if rem_ans == 'n':
            rep_ans = raw_input("Do you want to replace all outliers with the median value (y/n)? ")

        if rem_ans not in ['y', 'n'] or rep_ans not in ['y', 'n', ""]:
            print(RED + "Invalid response." + RESET)
            sys.exit(1)

        if rem_ans == 'n' and rep_ans == 'n':
            print("Skipping outliers")
            return

        quantiles = self.__src_df.quantile([0.25, 0.75], axis=0).values  # axis 0 for column-wise; 1 for row-wise
        minimums = self.__src_df.min(axis=0).values
        iqrs = []  # inter quartile ranges for each column
        for ix in xrange(len(quantiles[0])):
            # calc the inter quartile range
            iqr = quantiles[1][ix] - quantiles[0][ix]
            # calc the lower and upper bounds for outliers
            lower, upper = (quantiles[0][ix] - 1.5 * iqr), (quantiles[1][ix] + 1.5 * iqr)
            if not isinstance(minimums[ix], str) and minimums[ix] >= 0.00 > lower:
                lower = 0
            iqrs.append({"lower": lower, "upper": upper})

        medians = self.__src_df.median(axis=0).values
        row_ix = 0
        outlier_count = 0
        for rec in self.__src_df.values:
            for col in range(len(rec)):
                if col < len(iqrs) and not isinstance(rec[col], str):
                    if iqrs[col]["upper"] != 0 and (rec[col] <= iqrs[col]["lower"] or rec[col] >= iqrs[col]["upper"]):
                        outlier_count += 1
                        if rem_ans == 'y':
                            self.__src_df.drop(self.__src_df.index[row_ix])
                        elif rep_ans == 'y':
                            rec[col] = medians[col]

            row_ix += 1
        print(str(outlier_count) + " outliers were found and successfully dealt with.")

    def __dept_plot(self):
        departments = np.unique(self.__src_df["sales"])
        x = np.arange(len(departments))
        counts = []
        for dept in departments:
            cond1 = self.__src_df["sales"].map(lambda y: y == dept)
            cond2 = self.__src_df["left"].map(lambda y: y == 1)
            counts.append(len(self.__src_df[cond1 & cond2]))
        sns.set(palette="husl")
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts)
        fig.canvas.set_window_title('Department')
        plt.title("The number of employees that leave per department")
        plt.xlabel('Department')
        plt.ylabel('Number of employees')
        plt.xticks(x, departments)
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color='m', fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/department.png', bbox_inches='tight')

    def __salary_plot(self):
        salaries = np.unique(self.__src_df["salary"])
        x = np.arange(len(salaries))
        counts = []
        for dept in salaries:
            cond1 = self.__src_df["salary"].map(lambda y: y == dept)
            cond2 = self.__src_df["left"].map(lambda y: y == 1)
            counts.append(len(self.__src_df[cond1 & cond2]))
        sns.set()
        colors = plt.cm.BuPu(np.linspace(0, 0.5, len(salaries)))
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts, color=colors)
        fig.canvas.set_window_title('Salary')
        plt.title("The number of employees that leave per salary range")
        plt.xlabel('Salary Range')
        plt.ylabel('Number of employees')
        plt.xticks(x, salaries)
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color='m', fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/salary.png', bbox_inches='tight')

    def __project_hrs_promotion_plot(self):
        # 3.803054 -> mean for number_projects
        cond1 = self.__src_df["number_project"].map(lambda y: y >= 3.803054)  # more than mean
        # 201.050337 -> mean for avg_monthly_hrs
        cond2 = self.__src_df["average_montly_hours"].map(lambda y: y >= 201.050337)  # more than mean
        cond3 = self.__src_df["promotion_last_5years"].map(lambda y: y != 1)
        left_cond = self.__src_df["left"].map(lambda y: y == 1)
        stayed_cond = self.__src_df["left"].map(lambda y: y == 0)
        counts = [len(self.__src_df[cond1 & cond2 & cond3 & stayed_cond]),
                  len(self.__src_df[cond1 & cond2 & cond3 & left_cond])]
        x = np.arange(2)
        c = sns.color_palette("husl", 8)
        sns.set(palette="Greens_d")
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts)
        fig.canvas.set_window_title('Overworked and Unrecognised')
        plt.title("Overworked and unrecognised employee position")
        plt.xlabel('Overworked and Unrecognised employees')
        plt.ylabel('Number of employees')
        plt.xticks(x, ("Stayed", "Left"))
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color=c[6], fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/overworked_unrecognised.png', bbox_inches='tight')

    def __project_hrs_salary_plot(self):
        # 3.803054 -> mean for number_projects
        cond1 = self.__src_df["number_project"].map(lambda y: y >= 3.803054)  # more than mean
        # 201.050337 -> mean for avg_monthly_hrs
        cond2 = self.__src_df["average_montly_hours"].map(lambda y: y >= 201.050337)  # more than mean
        cond3 = self.__src_df["salary"].map(lambda y: y != "high")
        left_cond = self.__src_df["left"].map(lambda y: y == 1)
        stayed_cond = self.__src_df["left"].map(lambda y: y == 0)
        counts = [len(self.__src_df[cond1 & cond2 & cond3 & stayed_cond]),
                  len(self.__src_df[cond1 & cond2 & cond3 & left_cond])]
        x = np.arange(2)
        c = sns.color_palette("husl", 8)
        sns.set()
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts, color=c[1])
        fig.canvas.set_window_title('Overworked and Undervalued')
        plt.title("Overworked and undervalued employee position")
        plt.xlabel('Overworked and Undervalued employees')
        plt.ylabel('Number of employees')
        plt.xticks(x, ("Stayed", "Left"))
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color=c[3], fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/overworked_undervalued.png', bbox_inches='tight')

    def __accident_plot(self):
        cond = self.__src_df["Work_accident"].map(lambda y: y >= 0)
        left_cond = self.__src_df["left"].map(lambda y: y == 1)
        stayed_cond = self.__src_df["left"].map(lambda y: y == 0)
        counts = [len(self.__src_df[cond & stayed_cond]),
                  len(self.__src_df[cond & left_cond])]
        x = np.arange(2)
        c = sns.color_palette("hls", 8)
        sns.set()
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts, color=c[0])
        fig.canvas.set_window_title('Work Accident')
        plt.title("Effect of work accident on employees")
        plt.xlabel('Work accident factor')
        plt.ylabel('Number of employees')
        plt.xticks(x, ("Stayed", "Left"))
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color=c[5], fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/work_accident.png', bbox_inches='tight')

    def __satisfaction_plot(self):
        # 0.612834 -> mean for satisfaction_level
        cond = self.__src_df["satisfaction_level"].map(lambda y: y <= 0.612834)  # less than mean
        left_cond = self.__src_df["left"].map(lambda y: y == 1)
        stayed_cond = self.__src_df["left"].map(lambda y: y == 0)
        counts = [len(self.__src_df[cond & stayed_cond]),
                  len(self.__src_df[cond & left_cond])]
        x = np.arange(2)
        c = sns.color_palette("hls", 8)
        sns.set()
        fig, ax = plt.subplots()
        _ = ax.bar(x, counts, color=c[2])  # below average satisfaction level stayed and left
        fig.canvas.set_window_title('Satisfaction Level')
        plt.suptitle("Effect of satisfaction level on employees")
        plt.xlabel('Low satisfaction level')
        plt.ylabel('Number of employees')
        plt.xticks(x, ("Stayed", "Left"))
        for i, v in enumerate(counts):
            ax.text(i, v, str(v), color=c[5], fontweight='bold')
        # plt.ion()
        # plt.show()
        plt.savefig('reports/satisfaction_level.png', bbox_inches='tight')
