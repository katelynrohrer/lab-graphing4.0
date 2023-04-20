import os
import cv2
import math
import csv
import json
from utils import *
import glob
import numpy as np

# has a broader scope than just color
class Color:

    def __init__(self, color_name, two_marker=False):
        self.color_name = color_name
        self.hue =  (0, 0)
        self.sat =  (0, 0)
        self.val =  (0, 0)
        self.area = (0, 0)
        self.two_marker = two_marker

    def get_min(self):
        """
        Called within cv2.inRange() as second param to be unpacked
        """
        return self.hue[0], self.sat[0], self.val[0]
    
    def get_max(self):
        """
        Called within cv2.inRange() as third param to be unpacked
        """
        return self.hue[1], self.sat[1], self.val[1]
    
    def get_args(self):
        # mask = cv2.inRange(imageHSV, *clr.get_args())
        return (self.get_min(), self.get_max())
    
        


def initialize_data():
    pass


def find_files(directory):
    files = glob.glob(f"{directory}/**")
    return files


def get_config():
    """
    Attempts to load a settings.json file. If none exists, creates one and 
    prompts user to enter preferences to store

    :return: dictionary of config options
    """
    config_file = 'video_settings.json'

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        data_source = input("Enter data folder path: ")
        data_destination = input("Enter the destination path: ")

        config = {"data_source": data_source,
                  "data_destination": data_destination}
        
        with open(config_file, 'w') as f:
            json.dump(config, f)

    return config


def main(rotate=False):
    video_path = "ShoulderAA.Cam1.SSI2F.Run2.MOCA.8:9:22.Fast copy.MOV"
    two_marker_orientation = "horizontal"

    # load config and set directory
    config = get_config()
    DATA_DIR = config["data_source"]
    os.chdir(DATA_DIR)

    # load files from DATA_DIR
    files = find_files(DATA_DIR)

        



if __name__ == "__main__":
    main()
