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
import sys
import pandas as pd
import numpy as np


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
            print("Succesfully read file: " + dataset_name)
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

    def report(self, file_name):
        """
        Todo:
            Summarize EDA to file_name
        Params:
            file_name -> Type: String
        Returns:
            Void    
        """
        pass

    ##### Helper Methods ##### 

    def __find_missing_values(self):
        """
        Todo:
            Find the missing values for each coloumn in the dataset.
            Ask the user whether, for all coloumns, to interporlate the median (nominal) or mode (categorical)
            to replace the missing values.
            If not, ask whether, to interporlate the median (nominal) or mode (categorical)
            to replace the missing values for each coloumn.
        Params:
            No parameters
        Returns:
            Void
        """
        pass
    
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
        temp.drop_duplicates()
        new_count = len(temp)
        if new_count == old_count:
            print("No duplicate records found.")
            return
        answer = raw_input("Do you want to keep all duplicate records (y/n)? ")
        if answer == 'n':
            self.__src_df.drop_duplicates()
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
        pass