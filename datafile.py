import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.errors import InvalidIndexError
from scipy.signal import argrelextrema
from utils import *
from title import *
from angle_utils import *


class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.info = Title(filename)
        self.df = pd.read_csv(filename)
        self.add_seconds()
        self.make_wrist_ok()
        self.make_green_elbow_ok()

    def make_angles_ok(self):
        if "Angles" in self.df.columns:
            print(f"fixed angles for {self.info}")
            self.df.rename(columns={'Angles': 'angles'},inplace=True)
        if "angles" not in self.df.columns:
            print(f"Angles not in {self.df.columns} {self.info}")

    def make_wrist_ok(self):
        if "Wrist Pink X" in self.df.columns:
            self.df.rename(columns={'Wrist Pink X': 'Hand Pink X'},inplace=True)
        if "Wrist Pink Y" in self.df.columns:
            self.df.rename(columns={'Wrist Pink Y': 'Hand Pink Y'},inplace=True)

    def make_green_elbow_ok(self):
        if "Green X" in self.df.columns and self.info[MOTION] == "bicepc":
            self.df.rename(columns={'Green X': 'Elbow Green X'},inplace=True)
        if "Green Y" in self.df.columns and self.info[MOTION] == "bicepc":
            self.df.rename(columns={'Green Y': 'Elbow Green Y'},inplace=True)

    def validate_title(self):
        v_origins = ["moca", "biostamp"]
        v_motions = ["bicepc", "bodyl", "chestaa", "fingerp", "shoulderaa", "shoulderfe"]
        v_subjects = ["cg1f", "ch2m", "es3f", "gsp1m", "ssi2f", "ya3m"]
        v_muscles = ["forearm", "bicep", "brachio", "cspine", "midspine", "deltoid", "femor", "index", "thumb", "tricep"]
        v_runs = ["r1slow", "r1fast", "r2slow", "r2fast", "r3slow", "r3fast"]
        v_mode = ["angular", "linear", "all"]

        if self.info[ORIGIN] not in v_origins:
            print(f"INVALID ORIGIN FOR {self.info.filename}: {self.info[ORIGIN]}")
        if self.info[MOTION] not in v_motions:
            print(f"INVALID MOTION FOR {self.info.filename}: {self.info[MOTION]}")
        if self.info[SUBJECT] not in v_subjects:
            print(f"INVALID SUBJECT FOR {self.info.filename}: {self.info[SUBJECT]}")
        if self.info[ORIGIN] == "biostamp":
            if self.info[MUSCLE] not in v_muscles:
                print(f"INVALID MUSCLE FOR {self.info.filename}: {self.info[MUSCLE]}")
        if self.info[MODE] not in v_mode:
            print(f"INVALID MODE FOR {self.info.filename}: {self.info[MODE]}")
        if self.info[RUN] not in v_runs:
            print(f"INVALID RUN FOR {self.info.filename}: {self.info[RUN]}")
        
    
    def del_unnamed(self):
        self.df.drop("Unnamed: 0", axis=1, inplace=True)

    def print_title(self):
        print(self.info)

    def add_angles(self, debug=False):
        stamps = stamps_from_motion(self.info[MOTION])
        columns = columns_from_stamps(stamps, self.df.columns)

        for col in columns:
            if col not in self.df.columns:
                print(f"ERROR | {self.info} did not have column {col}")
                return

        if len(columns) == 4:
            self.df['angles'] = self.df.apply(lambda row: self.adjust_angles(
                row[columns[0]], row[columns[1]],
                row[columns[2]], row[columns[3]],
                None, None, columns, debug), axis=1)

        elif len(columns) == 6:
            self.df['angles'] = self.df.apply(lambda row: self.adjust_angles(
                row[columns[0]], row[columns[1]],
                row[columns[2]], row[columns[3]],
                row[columns[4]], row[columns[5]], columns, debug), axis=1)

    def adjust_angles(self, pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y, columns, debug):

        if snd_x is None:
            snd_x = self.df[columns[2]][0]
        if snd_y is None:
            snd_y = self.df[columns[3]][0]

        if self.info[MOTION] == "chestaa":
            forearm_cross = self.df[columns[3]][0]  # init forearm y
            shoulder_cross = self.df[columns[0]][0]

            angle = calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)

            if fst_y < forearm_cross and pivot_x > shoulder_cross and not debug:  # pt lower than init
                angle *= -1
            return angle

        elif self.info[MOTION] == "shoulderfe":
            forearm_cross = self.df[columns[2]][0]  # init x forearm
            shoulder_cross = self.df[columns[1]][0]  # init y shoulder

            angle = calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)
            if fst_x < forearm_cross and pivot_y < shoulder_cross and not debug:  # pt left of init and lower than shoulder
                angle *= -1

            return angle

        elif self.info[MOTION] == "shoulderaa":
            forearm_cross = self.df[columns[2]][0]  # init x forearm
            shoulder_cross = self.df[columns[1]][0]  # init y shoulder

            angle = calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)
            if fst_x > forearm_cross and pivot_y < shoulder_cross and not debug:  # pt right of init and lower than shoulder
                angle *= -1

            return angle

        elif self.info[MOTION] == "bicepc":
            cross_point = self.df[columns[5]][0]  # init y forearm

            angle = calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)
            if fst_y < cross_point and not debug:  # pt lower than init
                angle *= -1

            return angle

        elif self.info[MOTION] == "fingerp":
            return calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)

        elif self.info[MOTION] == "bodyl":
            cross_point = self.df[columns[2]][0]  # init c-spine x

            angle = calculate_angle(pivot_x, pivot_y, fst_x, fst_y, snd_x, snd_y)
            if fst_x > cross_point and not debug:  # pt right of init
                angle *= -1

            return angle

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
            ("gsp1m", "chestaa"): 0.3,
            ("gsp1m", "shoulderfe"): 0.3,
            ("gsp1m", "shoulderaa"): 0.26,
            ("gsp1m", "bicepc"): 0.265,
            ("gsp1m", "fingerp"): 0.09,
            ("gsp1m", "bodyl"): 0.19,

            ("ch2m", "chestaa"): 0.3,
            ("ch2m", "shoulderfe"): 0.345,
            ("ch2m", "shoulderaa"): 0.28,
            ("ch2m", "bicepc"): 0.315,
            ("ch2m", "fingerp"): 0.095,
            ("ch2m", "bodyl"): 0.25,

            ("ya3m", "chestaa"): 0.3,
            ("ya3m", "shoulderfe"): 0.3,
            ("ya3m", "shoulderaa"): 0.3,
            ("ya3m", "bicepc"): 0.34,
            ("ya3m", "fingerp"): 0.095,
            ("ya3m", "bodyl"): 0.25,

            ("cg1f", "chestaa"): 0.28,
            ("cg1f", "shoulderfe"): 0.28,
            ("cg1f", "shoulderaa"): 0.23,
            ("cg1f", "bicepc"): 0.27,
            ("cg1f", "fingerp"): 0.09,
            ("cg1f", "bodyl"): 0.27,

            ("es3f", "chestaa"): 0.275,
            ("es3f", "shoulderfe"): 0.25,
            ("es3f", "shoulderaa"): 0.245,
            ("es3f", "bicepc"): 0.26,
            ("es3f", "fingerp"): 0.08,
            ("es3f", "bodyl"): 0.275,

            ("ssi2f", "chestaa"): 0.304,
            ("ssi2f", "shoulderfe"): 0.22,
            ("ssi2f", "shoulderaa"): 0.25,
            ("ssi2f", "bicepc"): 0.27,
            ("ssi2f", "fingerp"): 0.08,
            ("ssi2f", "bodyl"): 0.254
        }

        e_to_h_motions = ["chestaa", "shoulderfe", "shoulderaa", "bicepc"]
        if self.info[MOTION] in e_to_h_motions:
            fst_x_col = [col for col in self.df.columns if 'elbow' in col.lower() and ' x' in col.lower()]
            fst_y_col = [col for col in self.df.columns if 'elbow' in col.lower() and ' y' in col.lower()]
            snd_x_col = [col for col in self.df.columns if 'hand' in col.lower() and ' x' in col.lower()]
            snd_y_col = [col for col in self.df.columns if 'hand' in col.lower() and ' y' in col.lower()]
        elif self.info[MOTION] == "fingerp":
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
            limb_len_m = lens[(self.info[SUBJECT], self.info[MOTION])]
        except KeyError:
            print(f"Length not found {self.info} {self.info[MOTION]}.")
            return

        limb_len_px = math.sqrt((side1 ** 2) + (side2 ** 2))
        scale = limb_len_m / limb_len_px

        x_cols = [col for col in self.df.columns if 'x' in col.lower()]
        y_cols = [col for col in self.df.columns if 'y' in col.lower()]

        for col in x_cols:
            self.df.loc[:, f"{col} meters"] = self.df[col] * scale
        for col in y_cols:
            self.df.loc[:, f"{col} meters"] = self.df[col] * (scale*-1)

    def get_angle_cor(self, **kwargs):
        other = DataFile(self.info.corresponding_bs())
        self_col = "angles"
        other_col = ""
        match self.info[MOTION]:
            case "bicepc":
                other_col = "gyro disp y (deg)"
            case "fingerp":
                other_col = "gyro disp y (deg)"
            case "chestaa":
                other_col = "gyro disp z (deg)"
            case "shoulderfe":
                other_col = "gyro disp z (deg)"
            case "bodyl":
                other_col = "gyro disp z (deg)"
            case "shoulderaa":
                other_col = "gyro disp z (deg)"
        return self.get_correlation(self_col, other, other_col, **kwargs)


    def get_correlation(self, self_col, other, other_col, graph=False, graph_delta=False,
                        save_dir="",suffix=""):
        if self_col not in self.df.columns:
            print(f"Column {self_col} not found in {self.filename}")
            print(f"  motion: {self.info[MOTION]}")
            raise InvalidIndexError
        if other_col not in other.df.columns:
            print(f"Column {other_col} not found in {other.filename}")
            print(f"  motion: {other.info[MOTION]}")
            raise InvalidIndexError

        self.trim_same_epoch(other)

        # Resample and remove any y-offset between the two
        self.resample()
        self.offset_zero(self_col)
        other.resample()
        other.offset_zero(other_col)
        # TODO: remove insane hardcoded negative multiplication
        # other.df[other_col] = other.df[other_col].apply(lambda x: -x)

        def corr_offset(s1, s2, of):
            s1, s2 = offset(s1, s2, of)
            corr = s1.corr(s2)
            return corr
        # Find the offset which maximizes correlation
        s1 = self.df[self_col]
        s2 = other.df[other_col]
        a = -100
        b = 100
        corr, best_offset = maximize(lambda x: corr_offset(s1,s2,x), a, b)

        # Get output dataset
        s1, s2 = offset(s1, s2, best_offset)
        deltas = s1 - s2
        avg_delta = deltas.mean()
        rmse = (s1 - s2)**2
        rmse = math.sqrt(rmse.mean())

        if graph:
            ax = s1.plot()
            s2.plot(ax=ax)
        if graph_delta:
            deltas.plot()

        if save_dir != "":
            short = f"{self.info.shortname[:-4]}.{suffix}.png"
            dest = f"{save_dir}{os.sep}{short}"
            necessary_dirs = os.sep.join(dest.split(os.sep)[:-1])
            os.makedirs(necessary_dirs, exist_ok=True)
            plt.savefig(dest)
            plt.close()

        return best_offset, corr, avg_delta, rmse

    def trim_same_epoch(self, other):
        this_start = self.df["Timestamp (microseconds)"].iloc[0]
        other_start = other.df["Timestamp (microseconds)"].iloc[0]

        if this_start < other_start:  # if this started first
            new_start = this_start
            i = 0
            while new_start <= other_start:
                if i == len(self.df["Timestamp (microseconds)"]):
                    print(f"Error correlating times. No adjustment made. {self.info}")
                    return
                new_start = self.df["Timestamp (microseconds)"].iloc[i]
                i += 1
            # cropping df based on timestamp value
            self.df = self.df.loc[i:]
            self.df.reset_index(drop=True, inplace=True)
            self.add_seconds()

        else:  # if other started first
            new_start = other_start
            i = 0
            while new_start <= this_start:
                if i == len(other.df["Timestamp (microseconds)"]):
                    print(f"Error correlating times. No adjustment made. {self.info}")
                    return
                new_start = other.df["Timestamp (microseconds)"].iloc[i]
                i += 1
            other.df = other.df.loc[i:]
            other.df.reset_index(drop=True, inplace=True)
            other.add_seconds()


    def add_seconds(self):
        df = self.df
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


    def graph(self, *axes, ax=None, extrema=False, show=True, save_dir="", suffix=""):
        df = self.df

        if ax is None:
            _, ax = plt.subplots()

        for axis in axes:
            if axis not in self.df.columns:
                # print(f"Cannot graph {axis} for {self.info}")
                continue
            if extrema: 
                self.plot_extrema(axis)
            df.plot(x="Seconds",y=axis, kind="line", ax=ax)

        plt.title(str(self.info))

        if show:
            plt.show()
        if save_dir != "":
            short = f"{self.info.shortname[:-4]}.{suffix}.png"
            dest = f"{save_dir}{os.sep}{short}"
            necessary_dirs = os.sep.join(dest.split(os.sep)[:-1])
            os.makedirs(necessary_dirs, exist_ok=True)
            plt.savefig(dest)
            plt.close()

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
        df.iloc[ilocs_max][column].plot(x="Seconds",style="v", lw=10, color="green")
        df.iloc[ilocs_min][column].plot(x="Seconds",style="^", lw=10, color="red")

        # draw the average line of the extrema
        top_line = df.iloc[ilocs_max][column].mean()
        bot_line = df.iloc[ilocs_min][column].mean()
        if draw_line:
            plt.axhline(y=top_line, color="g", linestyle="-")
            plt.axhline(y=bot_line, color="r", linestyle="-")

        return top_line, bot_line
    
    def __str__(self):
        return f"DataFile: \n  {str(self.info)}"

    def __getitem__(self, item):
        return self.df[item]
