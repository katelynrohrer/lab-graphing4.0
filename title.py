import os

class Title:
    def __init__(self, filename):
        self.filename = filename
        path_split = filename.split(os.sep)
        trial_info = path_split[-1].split(".")
        trial_info = [part for part in trial_info if part != ""]

        self.motion = trial_info[0]
        self.muscle = trial_info[1]


        motions = {"ChestAA": "Chest Abduction/Adduction",
                   "ShoulderFE": "Shoulder Flexion/Extension",
                   "ShoulderAA": "Shoulder Abduction/Adduction",
                   "BicepC": "Bicep Curl",
                   "FingerP": "Finger Pinch",
                   "BodyLean": "Body Lean"}

        muscles = {"Bicep": "Bicep",
                   "Brachio": "Brachioradialis",
                   "Forearm": "Forearm",
                   "Thumb": "Thumb"}

        if (self.motion in motions):
            self.motion = motions[self.motion]
        if (self.muscle in muscles):
            self.muscle = muscles[self.muscle]


    def __str__(self):
        """
        Builds title and styles it correctly.
        :param chosen_file: Str file name
        :param y_choice: Str axis to be graphed
        :return: Str graph title
        """

        # split_words = y_choice.lower().split()
        # axis = split_words[2]
        #
        # axes = {"x": "Vertical",
        #           "y": "Horizontal",
        #           "z": "Depth"}
        #
        # if (axis in axes):
        #     axis = axes[axis]

        return f"{self.motion}: {self.muscle}"

