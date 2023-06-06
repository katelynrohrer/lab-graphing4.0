import pandas as pd
# import numpy as np
import os
import json
import sys
import matplotlib.pyplot as plt
from glob import glob
from title import *
from datafile import DataFile
from search import Search
from utils import *
from pprint import pprint

def newf(filename=""):
    if filename == "":
        filename = prompt("gum file")
    print(filename)
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
        data_folder = input("Enter data folder path: ")
        image_folder = input("Enter image folder path: ")
        
        config = {"data_folder": data_folder,
                  "image_folder": image_folder}
        
        with open(config_file, 'w') as f:
            json.dump(config, f)

    return config

def abbrevs(*dfs):
    global abbrevdict
    cols = []
    for file in dfs:
        cols += list(file.df.columns)
    abbrevs = abbrev(cols)
    for key in abbrevs:
        exec(f'global {key}\n{key} = "{abbrevs[key]}"')

def main():
    global config
    # load config and set directory
    config = get_config()
    DATA_DIR = config["data_folder"]
    os.chdir(DATA_DIR)

    # p  ut matplotlib in interactive mode
    plt.ion()

if __name__ == "__main__":
    main()
