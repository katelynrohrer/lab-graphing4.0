import pandas as pd
import os
import json
import sys
import matplotlib.pyplot as plt
from single_angles import *
from manipulate_batch import *
from title import Title 
from datafile import DataFile
from utils import *
from pprint import pprint

    

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

    plt.title(str(Title(filename)))
    plt.xlabel("Time (s)")
    plt.ylabel(y_choice)


def newf(filename=""):
    if filename == "":
        filename = prompt("gum file")
    return DataFile(filename)


def get_config():
    """
    Attempts to load a settings.json file. If none exists, creates one and 
    prompts user to enter preferences to store

    :return: dictionary of config options
    """
    CONFIG_FILE = 'settings.json'

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        folder_name = input("Enter data folder path: ")
        
        config = {"data_folder": folder_name}
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    return config

def main():
    # load config and set directory
    config = get_config()
    DATA_DIR = config["data_folder"]
    os.chdir(DATA_DIR)

    # put matplotlib in interactive mode
    plt.ion()

    # Get file to operate on
    if "-f" in sys.argv:
        arg_pos = sys.argv.index("-f") + 1
        chosen_file = sys.argv[arg_pos]
    else:
        chosen_file = prompt("gum file")
        print(chosen_file)

    # Load data from file
    global df 
    df = DataFile(chosen_file)
    abbrevs = abbrev(df.columns)
    pprint(abbrevs)
    for key in abbrevs:
        if len(key) > 2:
            exec(f'global {key}\n{key} = "{abbrevs[key]}"')

    if "-t" in sys.argv:  # trim time
        arg_pos = sys.argv.index("-t") + 1
        range = sys.argv[arg_pos]
        start, stop = tuple(range.split(":"))
        df.trim(float(start), float(stop))

if __name__ == "__main__":
    main()
