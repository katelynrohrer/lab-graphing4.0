import os
import glob
from utils import *

ORIGIN = 0
MOTION = 1
SUBJECT = 2
MUSCLE = 3
CAMERA = 3
RUN = 4
MODE = 5

class Title:
    def __init__(self, filename):
        # splitting up file name into trial info
        self.filename = filename
        path_split = filename.split(os.sep)
        trial_info = path_split[-1].split(".")
        self.list = [part.lower() for part in trial_info][:-1]
        if (len(self.list) != 6):
            print(f"Incorrect number of elements from {self.filename} ({self.list})")

    def corresponding_bs(self):
        assert self[ORIGIN] == "moca", "Can currently only be run on moca files"
        
        folder = self.filename[:self.filename.rindex(os.sep)+1]

        corresponding_muscles = {"chestaa": "Brachio",
                                 "shoulderfe": "Forearm",
                                 "shoulderaa": "Forearm",
                                 "bicepc": "Forearm",
                                 "fingerp": "Index",
                                 "bodyl": "CSpine"
                                 }

        search_term = corresponding_muscles[self[MOTION]]
        file = folder + f"**{search_term}*angularDisp.csv"
        search = glob.glob(file)
    
        
        assert len(search) == 1, f"Error finding corresponding file {file}"

        return search[0]

    def __str__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        info = [self[MOTION], self[SUBJECT], self[RUN]]
        return " ".join(map(pretty, info))

    def __repr__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        return f"Title({', '.join(self.list)})"

    def csv_string(self):
        return (self[MOTION],self[SUBJECT],self[RUN][:2], self[RUN][2:])

    def __getitem__(self,index):
        if index >= len(self.list):
            print(f"Invalid title position: {index} for file {self.filename}")
            raise IndexError
        return self.list[index]
