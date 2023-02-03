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
    return df.iloc[start:stop]

def plot_extrema(df, column, margin=25, draw_line=True):
    ilocs_min = argrelextrema(df[column].values, np.less_equal, order=margin//2)[0]
    ilocs_max = argrelextrema(df[column].values, np.greater_equal, order=margin)[0]

    # filter elements that are peaks and plot
    df.iloc[ilocs_max][column].plot(style='v', lw=10, color='green');
    df.iloc[ilocs_min][column].plot(style='^', lw=10, color='red');

    # draw the average line of the extrema
    top_line = df.iloc[ilocs_max][column].mean()
    bot_line = df.iloc[ilocs_min][column].mean()
    if (draw_line):
        plt.axhline(y = top_line, color = 'g', linestyle = '-')
        plt.axhline(y = bot_line, color = 'r', linestyle = '-')

    return top_line, bot_line


def main():
    if "-f" in sys.argv:
        arg_pos = sys.argv.index("-f") + 1
        chosen_file = sys.argv[arg_pos]
    else:
        chosen_file = prompt("gum file")
        print(chosen_file)

    df = pd.read_csv(chosen_file)
    df.index = df[df.columns[0]]
    del df[df.columns[0]]

    if "-t" in sys.argv:
        arg_pos = sys.argv.index("-t") + 1
        range = sys.argv[arg_pos]
        start, stop = tuple(range.split(":"))
        df = trim_data(df, int(start), int(stop))

    # create the column choices
    command = "gum choose"
    for col in df.columns:
        command += f' "{col}"'

    y_choice = prompt(command)

    df.plot(y=y_choice, kind="line")
    top, bottom = plot_extrema(df, y_choice, margin=120)
    print(top, bottom, top-bottom)

    plt.show()

main()

