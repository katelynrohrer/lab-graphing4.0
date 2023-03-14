import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from single_angles import *
from manipulate_batch import *
from title import *

def abbreviate(strings):
    retlist = []
    for string in strings:
        abbrev = ""
        index = 1
        for word in string.split():
            abbrev += word[:index]
        while abbrev in retlist:
            index+=1
            abbrev = ""

        retlist.append(abbrev)

def prompt(command):
    """
    Given a command for the shell, returns the output of the command as a
    string

    :param command: the terminal command to send

    :return: the output of the command, as a string
    """
    result = os.popen(command)
    retstring = result.readline()[:-1]
    result.close()

    return retstring


def trim(start, stop):
    """
    Trims the x-axis in terms of seconds
    :param df: Dataframe containing a ["Seconds"] column
    :param start: Start time int in seconds
    :param stop: Stop time int in seconds
    """
    global df
    df = df.loc[start:stop]


def plot_extrema(column, margin=25, draw_line=True):
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

def graph_single(filename):

    y_choice = "gyro vel y (dps)"

    df = pd.read_csv(filename)

    # Converting time into seconds
    if "MOCA" in filename:
        start_time = df["Timestamp (microseconds)"][0]
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x - start_time) 
        df["Seconds"] = df["Seconds"].apply(lambda x : x / 1000000)
    else:
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x / 1000000)
    df = df.set_index("Seconds")
    df.plot(y=y_choice, kind="line")

    plt.title(str(title))
    plt.xlabel("Time (s)")
    plt.ylabel(y_choice)

def reset():
    global df
    df = pd.read_csv(title.filename())

    if "MOCA" in title.filename():
        start_time = df["Timestamp (microseconds)"][0]
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x - start_time) 
        df["Seconds"] = df["Seconds"].apply(lambda x : x / 1000000)
    else:
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x / 1000000)
    df = df.set_index("Seconds")

def write():
    df.to_csv(title.filename())

def graph(*axes, extrema=False):
    axes_list = list(axes)

    _, ax = plt.subplots()

    for axis in axes_list:
        if extrema: 
            plot_extrema(axis)
        df.plot(y=axis, kind="line", ax=ax)

    plt.title(str(title))
    plt.show()

def main():
    os.chdir("/Users/jordan/Documents/Work/All-Lab-Data")

    if "-f" in sys.argv:
        arg_pos = sys.argv.index("-f") + 1
        chosen_file = sys.argv[arg_pos]
    else:
        chosen_file = prompt("gum file")
        print(chosen_file)

    global df
    global title
    df = pd.read_csv(chosen_file)
    title = Title(chosen_file)

    if "MOCA" in chosen_file:
        start_time = df["Timestamp (microseconds)"][0]
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x - start_time) 
        df["Seconds"] = df["Seconds"].apply(lambda x : x / 1000000)
    else:
        df["Seconds"] = df["Timestamp (microseconds)"].apply(lambda x : x / 1000000)
    df = df.set_index("Seconds")

    if "-t" in sys.argv:  # trim time
        arg_pos = sys.argv.index("-t") + 1
        range = sys.argv[arg_pos]
        start, stop = tuple(range.split(":"))
        trim(float(start), float(stop))

    # # create the column choices
    # command = "gum choose"
    # for col in df.columns:
    #     command += f' "{col}"'
    #
    # y_choice = prompt(command)
    #
    # if "-h" in sys.argv:  # crop height
    #     arg_pos = sys.argv.index("-h") + 1
    #     range = sys.argv[arg_pos]
    #     start, stop = tuple(range.split(":"))
    #     df.plot(y=y_choice, ylim=(float(start), float(stop)), kind="line")
    # else:
    #     df.plot(y=y_choice, kind="line")

    # top, bottom = plot_extrema(df, y_choice, margin=120)
    # print(top, bottom, top - bottom)
    #
    # plt.title(make_title(chosen_file, y_choice))
    # plt.xlabel("Time (s)")
    # plt.ylabel(y_choice)
    #
    # plt.show()

if __name__ == "__main__":
    main()
