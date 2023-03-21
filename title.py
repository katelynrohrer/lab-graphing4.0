import os

class Title:
    def __init__(self, filename):
        # splitting up file name into trial info
        self.filename = filename
        path_split = filename.split(os.sep)
        trial_info = path_split[-1].split(".")
        trial_info = [part.lower() for part in trial_info if part != "" and part != "csv"]


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
            self.motion, _, self.subject, self.run, _, self.date, self.speed, = trial_info
            self.measure = "disp"
            self.muscle = "undetermined"
        else:
            self.motion, self.muscle, self.subject, self.run, _, self.date, self.speed, self.measure = trial_info


        # attempts to make motion and muscles strs "pretty"
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

        if self.motion in motions:
            self.motion = motions[self.motion]
        if self.muscle in muscles:
            self.muscle = muscles[self.muscle]
        if self.origin in origins:
            self.origin = origins[self.origin]

    def title_str(self):
        """
        Builds title string for the graphs
        :return: Str title
        """

        # Removes muscle if undetermined
        if self.muscle == "undetermined":
            print_muscle = ""
        else:
            print_muscle = " " + self.muscle

        return f"{self.motion} " \
               f"{self.subject.upper()}" \
               f"{print_muscle} " \
               f"{self.run[0:3].capitalize()} {self.run[3]} " \
               f"{self.speed.capitalize()} "

    def __str__(self):
        """
        Builds a representation of all of the file information.
        :return: Info string
        """
        return f"Origin: {self.origin:^8} | " \
               f"Motion: {self.motion:^2} | " \
               f"Muscle: {self.muscle:^15} | " \
               f"Subject: {self.subject:^5} | " \
               f"Run: {self.run:^4} | " \
               f"Speed: {self.speed:^4} | " \
               f"Date: {self.date:^7} | " \
               f"Measure: {self.measure:^11} | " \
               f"Epoch: {str(self.epoch):^5s}"
