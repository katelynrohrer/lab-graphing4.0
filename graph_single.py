import pandas as pd
# import numpy as np
import os
import json
import sys
import matplotlib.pyplot as plt
from glob import glob
from title import Title 
from datafile import DataFile
from utils import *
from pprint import pprint

def matches_pat(terms, name):
    name = name.lower()
    for term in terms:
        term = term.lower()
        if term not in name:
            return False
    return True

def search(*terms, csv_only=True):
    terms = list(terms)
    if csv_only:
        terms.append(".csv")
    terms = map(str.lower, terms)

    match_fun = lambda x: False not in [term in x.lower() for term in terms]

    files = glob("./**", recursive=True)
    # cur_match = lambda x: matches_pat(terms, x)
    files = filter(match_fun, files)

    return list(files)

def make_dfs(filenames):
    return [DataFile(f) for f in filenames]
    
def apply(dfs, methodToRun, *args):
    for df in dfs:
        methodToRun(df, *args)

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
    config_file = 'settings.json'

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        folder_name = input("Enter data folder path: ")
        
        config = {"data_folder": folder_name}
        
        with open(config_file, 'w') as f:
            json.dump(config, f)

    return config

def abbrevs(*dfs):
    global abbrevs
    cols = []
    for df in dfs:
        cols += list(df.columns)
    abbrevs = abbrev(cols)
    pprint(abbrevs)
    for key in abbrevs:
        exec(f'global {key}\n{key} = "{abbrevs[key]}"')

def main():
    # load config and set directory
    config = get_config()
    DATA_DIR = config["data_folder"]
    os.chdir(DATA_DIR)

    # put matplotlib in interactive mode
    plt.ion()

if __name__ == "__main__":
    main()
