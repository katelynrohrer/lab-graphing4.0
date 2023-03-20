import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from utils import prompt
from title import *


class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.info = Title(filename)

        self.df = pd.read_csv(filename)
        self.columns = self.df.columns
        # self.df = self.df.set_index("Seconds")


    def add_seconds(self):
        df = self.df
        if "Seconds" not in df.columns:
            start_time = df["Timestamp (microseconds)"][0]
            df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x - start_time) 
            df["Seconds"] = df["Seconds"].apply(lambda x : x / 1000000)

        self.df = self.df.set_index("Seconds")

    def graph(self, *axes, extrema=False):
        df = self.df

        _, ax = plt.subplots()

        for axis in axes:
            if extrema: 
                self.plot_extrema(axis)
            df.plot(y=axis, kind="line", ax=ax)

        plt.title(str(self.info))
        plt.show()

    def write(self):
        self.df.to_csv(self.filename)

    def reset(self):
        self.df = pd.read_csv(self.filename)
        self.columns = self.df.columns
        # self.df = df.set_index("Seconds")

    def choose_col(self):
        command = "gum choose"
        for col in self.df.columns:
            command += f' "{col}"'

        return prompt(command)

    def trim(self, start, stop):
        """
        Trims the x-axis in terms of seconds
        :param df: Dataframe containing a ["Seconds"] column
        :param start: Start time int in seconds
        :param stop: Stop time int in seconds
        """
        self.df = self.df.loc[start:stop]

    def plot_extrema(self, column, margin=25, draw_line=True):
        df = self.df

        ilocs_min = argrelextrema(df[column].values, np.less_equal, order=margin // 2)[0]
        ilocs_max = argrelextrema(df[column].values, np.greater_equal, order=margin)[0]

        # filter elements that are peaks and plot
        df.iloc[ilocs_max][column].plot(style="v", lw=10, color="green")
        df.iloc[ilocs_min][column].plot(style="^", lw=10, color="red")

        # draw the average line of the extrema
        top_line = df.iloc[ilocs_max][column].mean()
        bot_line = df.iloc[ilocs_min][column].mean()
        if draw_line:
            plt.axhline(y=top_line, color="g", linestyle="-")
            plt.axhline(y=bot_line, color="r", linestyle="-")

        return top_line, bot_line
    
    def __str__(self):
        return f"DataFile: {self.info}"

    def __getitem__(self, item):
        return self.df[item]

