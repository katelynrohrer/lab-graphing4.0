import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema


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


def trim_data(df, start, stop):
    """
    Trims the x-axis in terms of seconds
    :param df: Dataframe containing a ["Seconds"] column
    :param start: Start time int in seconds
    :param stop: Stop time int in seconds
    :return: The time cropped dataframe
    """
    seconds = list(df["Seconds"])  # wasn't sure how to index into df
    start_index, stop_index = 0, len(seconds)-1
    for i in range(len(seconds)):
        if seconds[i] <= start:
            start_index = i
        if seconds[i] <= stop:
            stop_index = i
    return df.iloc[start_index:stop_index]


def plot_extrema(df, column, margin=25, draw_line=True):
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


def main():
    if "-f" in sys.argv:
        arg_pos = sys.argv.index("-f") + 1
        chosen_file = sys.argv[arg_pos]
    else:
        chosen_file = prompt("gum file")
        print(chosen_file)

    df = pd.read_csv(chosen_file)
    # Converting time into seconds
    ms = list(df[df.columns[0]])
    df["Seconds"] = [(item - ms[0]) / 1000000 for item in ms]
    df.index = df[df.columns[-1]]
    del df[df.columns[0]]

    if "-t" in sys.argv:  # trim time
        arg_pos = sys.argv.index("-t") + 1
        range = sys.argv[arg_pos]
        start, stop = tuple(range.split(":"))
        df = trim_data(df, int(start), int(stop))

    del df[df.columns[-1]]

    # create the column choices
    command = "gum choose"
    for col in df.columns:
        command += f' "{col}"'

    y_choice = prompt(command)
    # -- tried to get ylim to work here but the line kept disappearing
    # y_lim = []
    # if "-h" in sys.argv:  # crop height
    #     arg_pos = sys.argv.index("-h") + 1
    #     range = sys.argv[arg_pos]
    #     y_lim = tuple(range.split(":"))
    #     df.plot(y=y_choice, ylim=(start, stop), kind="line")
    # else:
    df.plot(y=y_choice, kind="line")

    top, bottom = plot_extrema(df, y_choice, margin=120)
    print(top, bottom, top - bottom)

    plt.title(make_title(chosen_file, y_choice))
    plt.xlabel("Time (s)")
    plt.ylabel(y_choice)

    plt.show()

def make_title(chosen_file, y_choice):
    """
    Builds title and styles it correctly.
    :param chosen_file: Str file name
    :param y_choice: Str axis to be graphed
    :return: Str graph title
    """
    path_split = chosen_file.split(os.sep)
    trial_info = path_split[-1].split(".")
    trial_info = [part for part in trial_info if part != ""]

    motion = trial_info[0]
    muscle = trial_info[1]

    split_words = y_choice.lower().split()
    axis = split_words[1]

    motions = {"ChestAA": "Chest Abduction/Adduction",
               "ShoulderFE": "Shoulder Flexion/Extension",
               "ShoulderAA": "Shoulder Abduction/Adduction",
               "BicepC": "Bicep Curl",
               "FingerP": "Finger Pinch",
               "BodyLean": "Body Lean"}

    muscles = {"Bicep": "Bicep",
               "Brachio": "Brachioradialis",
               "Forearm": "Forearm"}

    axises = {"x": "Vertical",
              "y": "Horizontal",
              "z": "Depth"}

    return f"{motions[motion]}: {muscles[muscle]} {axises[axis]} Axis"

main()
