import os
import glob

class Title:
    def __init__(self, filename):
        # splitting up file name into trial info
        self.filename = filename
        path_split = filename.split(os.sep)
        trial_info = path_split[-1].split(".")
        trial_info = [part.lower() for part in trial_info if part != "" and part != "csv"]
        self.origin = ""

        # checking for moca vs biostamp data
        if "moca" in trial_info:
            self.origin = "moca"
            self.epoch = False
            # if epoch file, remove epoch title and set flag to true
            if "epoch" in trial_info:
                trial_info = trial_info[:-1]
                self.epoch = True
        elif "biostamp" in trial_info:
            self.origin = "bio"
            self.epoch = True

        # correlating trial info with object attributes
        if self.origin == "moca":
            try:
                self.motion, _, self.subject, self.run, _, self.date, self.speed = tuple(trial_info)
            except:
                print(f"FAILED TO GEN TITLE FOR {self.filename}")
                return
            self.measure = "disp"
            self.muscle = "undetermined"
        else:
            try:
                self.motion, self.muscle, self.subject, self.run, _, self.date, self.speed, self.measure = tuple(trial_info)
            except:
                print(f"FAILED TO GEN TITLE FOR {self.filename}")
                return

    def corresponding_bs(self):
        assert self.origin == "moca", "Can currently only be run on moca files"
        
        if self.subject == "ssi2f":
            return

        folder = self.filename[:self.filename.rindex(os.sep)+1]

        corresponding_muscles = {"chestaa": "Forearm",
                                 "shoulderfe": "Forearm",
                                 "shoulderaa": "Forearm",
                                 "bicepc": "Forearm",
                                 "fingerp": "Index",
                                 "bodylean": "CSpine"
                                 }

        search_term = corresponding_muscles[self.motion]
        file = folder + f"**{search_term}*angularDisp.csv"
        search = glob.glob(file)
    
        
        assert len(search) == 1, f"Error finding corresponding file {file}"

        return search

    def prettify(self, str):
        names = {"chestaa": "Chest Abduction/Adduction",
                 "shoulderfe": "Shoulder Flexion/Extension",
                 "shoulderaa": "Shoulder Abduction/Adduction",
                 "bicepc": "Bicep Curl",
                 "fingerp": "Finger Pinch",
                 "bodylean": "Body Lean",
                 "brachio": "Brachioradialis",
                 "cspine": "Cervical Spine",
                 "femor": "Biceps Femoris",
                 "midspine": "Mid-Thoracic Spine",
                 "deltoid": "Medial Deltoid",
                 "moca": "MOCA"
                 }
        if str in names:
            return names[str]
        else:
            return str.title()

    def title_str(self):
        """
        Builds title string for the graphs
        :return: Str title
        """
        print_motion, print_muscle = self.motion, self.muscle
        if self.motion in Title.motions:
            print_motion = Title.motions[self.motion]
        if self.muscle in Title.muscles:
            print_muscle = Title.muscles[self.muscle]

        # Removes muscle if undetermined
        if print_muscle != "undetermined":
            print_muscle = " " + self.muscle

        return f"{print_motion} " \
               f"{self.subject.upper()}" \
               f"{print_muscle} " \
               f"{self.run[0:3].capitalize()} {self.run[3]} " \
               f"{self.speed.capitalize()} "

    def __str__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        print_motion, print_muscle = self.motion, self.muscle
        if self.motion in Title.motions:
            print_motion = Title.motions[self.motion]
        if self.muscle in Title.muscles:
            print_muscle = Title.muscles[self.muscle]

        return f"Motion: {print_motion} | " \
               f"Muscle: {print_muscle} | " \
               f"Subject: {self.subject}" \

    def __repr__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        print_motion, print_muscle, print_origin = \
            self.motion, self.muscle, self.origin

        if self.motion in Title.motions:
            print_motion = Title.motions[self.motion]
        if self.muscle in Title.muscles:
            print_muscle = Title.muscles[self.muscle]
        if self.origin in Title.origins:
            print_origin = Title.origins[self.origin]

        return f"Origin: {print_origin:^8} | " \
               f"Motion: {print_motion:^2} | " \
               f"Muscle: {print_muscle:^15} | " \
               f"Subject: {self.subject:^5} | " \
               f"Run: {self.run:^4} | " \
               f"Speed: {self.speed:^4} | " \
               f"Date: {self.date:^7} | " \
               f"Measure: {self.measure:^11} | " \
               f"Epoch: {str(self.epoch):^5s} |"

    def csv_string(self):
        return (self.motion,self.subject,self.run,self.speed)

    def pprint(self):
        """
        Builds a representation of all of the file information.
        *but* in a form that fits all within 80 characters, per
        each of the three lines

        :return: Info string 
        """
        print_motion, print_muscle, print_origin = \
            self.motion, self.muscle, self.origin

        if self.motion in Title.motions:
            print_motion = Title.motions[self.motion]
        if self.muscle in Title.muscles:
            print_muscle = Title.muscles[self.muscle]
        if self.origin in Title.origins:
            print_origin = Title.origins[self.origin]

        return f"\t| Origin: {print_origin:^8} | " \
               f"Motion: {print_motion:^2} | " \
               f"\n\t| Muscle: {print_muscle:^15} | " \
               f"Subject: {self.subject:^5} | " \
               f"Run: {self.run:^4} | " \
               f"\n\t| Speed: {self.speed:^4} | " \
               f"Date: {self.date:^7} | " \
               f"Measure: {self.measure:^11} | " \
               f"Epoch: {str(self.epoch):^5s} |"


    motions = {"chestaa": "Chest Abduction/Adduction",
               "shoulderfe": "Shoulder Flexion/Extension",
               "shoulderaa": "Shoulder Abduction/Adduction",
               "bicepc": "Bicep Curl",
               "fingerp": "Finger Pinch",
               "bodylean": "Body Lean"}

    muscles = {"bicep": "Bicep",
               "brachio": "Brachioradialis",
               "forearm": "Forearm",
               "thumb": "Thumb",
               "index": "Index",
               "cspine": "Cervical Spine",
               "femor": "Biceps Femoris",
               "midspine": "Mid-Thoracic Spine",
               "tricep": "Tricep",
               "deltoid": "Medial Deltoid"}

    origins = {"bio": "Biostamp",
               "moca": "MOCA"}
