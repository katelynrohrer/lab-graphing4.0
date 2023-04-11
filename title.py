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
            print(f"Missing elements from {self.filename} ({self.list})")

    def corresponding_bs(self):
        assert self[MOTION] == "moca", "Can currently only be run on moca files"
        
        folder = self.filename[:self.filename.rindex(os.sep)+1]

        corresponding_muscles = {"chestaa": "Brachio",
                                 "shoulderfe": "Forearm",
                                 "shoulderaa": "Forearm",
                                 "bicepc": "Forearm",
                                 "fingerp": "Index",
                                 "bodylean": "CSpine"
                                 }

        search_term = corresponding_muscles[self[MOTION]]
        file = folder + f"**{search_term}*angularDisp.csv"
        search = glob.glob(file)
    
        
        assert len(search) == 1, f"Error finding corresponding file {file}"

        return search[0]

    def title_str(self):
        """
        Builds title string for the graphs
        :return: Str title
        """
        return f"{pretty(self[MOTION])} " \
               f"{self[SUBJECT].upper()} " \
               f"{pretty(self[MUSCLE])} " \
               f"{self[RUN]} " \

    def __str__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        return f"Motion: {pretty(self[MOTION])} | " \
               f"Muscle: {pretty(self[MUSCLE])} | " \
               f"Subject: {pretty(self[SUBJECT])}" \

    def __repr__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        return f"Origin: {pretty(self[ORIGIN]):^8} | " \
               f"Motion: {pretty(self[MOTION]):^2} | " \
               f"Muscle: {pretty(self[MUSCLE]):^15} | " \
               f"Subject: {self[SUBJECT]:^5} | " \
               f"Run: {self[RUN]:^4} | " \
               f"Mode: {self[MODE]:^4} | " \

    def csv_string(self):
        return (self[MOTION],self[SUBJECT],self[RUN][:2], self[RUN][2:])

    def __getitem__(self,index):
        return self.list[index]
