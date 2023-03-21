import pandas as pd
# import numpy as np
import os
import json
import sys
import matplotlib.pyplot as plt
from glob import glob
from title import Title 
from datafile import DataFile
from search import Search
from utils import *
from pprint import pprint

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
    for file in dfs:
        cols += list(file.df.columns)
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
