import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from utils import prompt
from title import *
from angle_utils import *


class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.info = Title(filename)
        self.df = pd.read_csv(filename)
        self.add_seconds()

    def del_unnamed(self):
        self.df.drop("Unnamed: 0", axis=1, inplace=True)

    def add_angles(self):
        stamps = stamps_from_motion(self.info.motion)
        columns = columns_from_stamps(stamps, self.df.columns)

        for col in columns:
            if col not in self.df.columns:
                print(f"ERROR | File did not have column {col}")
                return

        if len(columns) == 4:
            start_pos_1 = self.df[columns[2]][0]
            start_pos_2 = self.df[columns[3]][0]
            self.df['angles'] = self.df.apply(lambda row: calculate_angle(
                row[columns[0]], row[columns[1]], row[columns[2]], row[columns[3]],
                start_pos_1, start_pos_2), axis=1)

        elif len(columns) == 6:
            self.df['angles'] = self.df.apply(lambda row: calculate_angle(
                row[columns[0]], row[columns[1]], row[columns[2]], row[columns[3]],
                row[columns[4]], row[columns[5]]), axis=1)

    def offset_zero(self, col):
        df = self.df
        start = df[col][0]
        df[col] = df[col].apply(lambda x : x - start) 

    def offset(self, amt):
        self.df.set_index("Seconds",inplace=True)
        self.trim(amt, 10000000)
        self.df.reset_index(inplace=True)
        self.offset_zero("Seconds")

    def resample(self, sr="10000U"):
        self.df.index = pd.to_datetime(self.df["Seconds"],unit="s")
        self.df = self.df.resample(sr).mean()
        self.df = self.df.interpolate(method='linear')
        self.df.reset_index(drop=True,inplace=True)

    def px_to_m(self):
        """
        Finds conversion factor for pixels to meters and adds columns
        to the dataset for the meter scaled values.
        """
        # hard coded arm lengths
        lens = {
            ("gsp1m", "Chest Abduction/Adduction"): 0.3,
            ("gsp1m", "Shoulder Flexion/Extension"): 0.3,
            ("gsp1m", "Shoulder Abduction/Adduction"): 0.26,
            ("gsp1m", "Bicep Curl"): 0.265,
            ("gsp1m", "Finger Pinch"): 0.09,
            ("gsp1m", "Body Lean"): 0.19,

            ("ch2m", "Chest Abduction/Adduction"): 0.3,
            ("ch2m", "Shoulder Flexion/Extension"): 0.345,
            ("ch2m", "Shoulder Abduction/Adduction"): 0.28,
            ("ch2m", "Bicep Curl"): 0.315,
            ("ch2m", "Finger Pinch"): 0.095,
            ("ch2m", "Body Lean"): 0.25,

            ("ya3m", "Chest Abduction/Adduction"): 0.3,
            ("ya3m", "Shoulder Flexion/Extension"): 0.3,
            ("ya3m", "Shoulder Abduction/Adduction"): 0.3,
            ("ya3m", "Bicep Curl"): 0.34,
            ("ya3m", "Finger Pinch"): 0.095,
            ("ya3m", "Body Lean"): 0.25,

            ("cg1f", "Chest Abduction/Adduction"): 0.28,
            ("cg1f", "Shoulder Flexion/Extension"): 0.28,
            ("cg1f", "Shoulder Abduction/Adduction"): 0.23,
            ("cg1f", "Bicep Curl"): 0.27,
            ("cg1f", "Finger Pinch"): 0.09,
            ("cg1f", "Body Lean"): 0.27,

            ("es3f", "Chest Abduction/Adduction"): 0.275,
            ("es3f", "Shoulder Flexion/Extension"): 0.25,
            ("es3f", "Shoulder Abduction/Adduction"): 0.245,
            ("es3f", "Bicep Curl"): 0.26,
            ("es3f", "Finger Pinch"): 0.08,
            ("es3f", "Body Lean"): 0.275
        }

        e_to_h_motions = ["Chest Abduction/Adduction", "Shoulder Flexion/Extension", "Shoulder Abduction/Adduction", "Bicep Curl"]
        if self.info.motion in e_to_h_motions:
            fst_x_col = [col for col in self.df.columns if 'elbow' in col.lower() and ' x' in col.lower()]
            fst_y_col = [col for col in self.df.columns if 'elbow' in col.lower() and ' y' in col.lower()]
            snd_x_col = [col for col in self.df.columns if 'hand' in col.lower() and ' x' in col.lower()]
            snd_y_col = [col for col in self.df.columns if 'hand' in col.lower() and ' y' in col.lower()]
        elif self.info.motion == "Finger Pinch":
            fst_x_col = [col for col in self.df.columns if 'index' in col.lower() and ' x' in col.lower()]
            fst_y_col = [col for col in self.df.columns if 'index' in col.lower() and ' y' in col.lower()]
            snd_x_col = [col for col in self.df.columns if 'thumb' in col.lower() and ' x' in col.lower()]
            snd_y_col = [col for col in self.df.columns if 'thumb' in col.lower() and ' y' in col.lower()]
        else:  # else body lean
            fst_x_col = [col for col in self.df.columns if 'back' in col.lower() and ' x' in col.lower()]
            fst_y_col = [col for col in self.df.columns if 'back' in col.lower() and ' y' in col.lower()]
            snd_x_col = [col for col in self.df.columns if 'neck' in col.lower() and ' x' in col.lower()]
            snd_y_col = [col for col in self.df.columns if 'neck' in col.lower() and ' y' in col.lower()]

        side1 = float(self.df[fst_y_col].iloc[0]) - float(self.df[snd_y_col].iloc[0])
        side2 = float(self.df[fst_x_col].iloc[0]) - float(self.df[snd_x_col].iloc[0])

        try:
            limb_len_m = lens[(self.info.subject, self.info.motion)]
        except KeyError:
            print("Length not found.")
            return

        limb_len_px = math.sqrt((side1 ** 2) + (side2 ** 2))
        scale = limb_len_m / limb_len_px
        print(scale)

        x_cols = [col for col in self.df.columns if 'x' in col.lower()]
        y_cols = [col for col in self.df.columns if 'y' in col.lower()]

        for col in x_cols:
            self.df.loc[:, f"{col} meters"] = self.df[col] * scale
        for col in y_cols:
            self.df.loc[:, f"{col} meters"] = self.df[col] * scale

    def add_seconds(self):
        df = self.df
        if "Seconds" in df.columns:
            return
        if "time (s)" in df.columns:
            df["Seconds"] = df["time (s)"]
            df.drop("time (s)", axis=1, inplace=True)
        elif "Timestamp (microseconds)" in df.columns:
            start_time = df["Timestamp (microseconds)"][0]
            df["Seconds"] = df["Timestamp (microseconds)"].apply(
                lambda x: x - start_time)
            df["Seconds"] = df["Seconds"].apply(lambda x: x / 1000000)
        else:
            print(f"seconds not found for {self.filename}")


    def print_corr(self):
        self.info.corresponding_bs()


    def graph(self, *axes, ax=None, extrema=False):
        df = self.df

        if ax is None:
            _, ax = plt.subplots()

        for axis in axes:
            if extrema: 
                self.plot_extrema(axis)
            df.plot(x="Seconds",y=axis, kind="line", ax=ax)

        plt.title(str(self.info))
        plt.show()

        return ax

    def write(self):
        self.df.to_csv(self.filename, index=False)

    def reset(self):
        self.df = pd.read_csv(self.filename)
        self.add_seconds()


    def choose_col(self):
        command = "gum choose"
        for col in self.df.columns:
            command += f' "{col}"'

        return prompt(command)

    def trim(self, start, stop):
        """
        Trims the x-axis in terms of seconds
        :param df: Dataframe containing a ["Seconds"] column
        :param start: Start time int in seconds
        :param stop: Stop time int in seconds
        """
        self.df = self.df.loc[start:stop]

    def plot_extrema(self, column, margin=25, draw_line=True):
        df = self.df

        ilocs_min = argrelextrema(df[column].values, np.less_equal, order=margin // 2)[0]
        ilocs_max = argrelextrema(df[column].values, np.greater_equal, order=margin)[0]

        # filter elements that are peaks and plot
        df.iloc[ilocs_max][column].plot(style="v", lw=10, color="green")
        df.iloc[ilocs_min][column].plot(style="^", lw=10, color="red")

        # draw the average line of the extrema
        top_line = df.iloc[ilocs_max][column].mean()
        bot_line = df.iloc[ilocs_min][column].mean()
        if draw_line:
            plt.axhline(y=top_line, color="g", linestyle="-")
            plt.axhline(y=bot_line, color="r", linestyle="-")

        return top_line, bot_line
    
    def __str__(self):
        return f"DataFile: \n{self.info.pprint()}"

    def __getitem__(self, item):
        return self.df[item]

