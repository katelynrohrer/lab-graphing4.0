import pandas as pd
import os
import sys
import matplotlib.pyplot as plt


def prompt(command):
    """
    Given a command for the shell, returns the output of the command as a 
    string
    
    :param command: the terminal command to send
    
    :return: the output of the command, as a string
    """
    result = os.popen(command)
    retstring = result.readline()[:-1]
    result.close()

    return retstring


def prompt_for_stamps(cols):
    """
    Given a list of column names, returns a tuple of the "stamp" names
    
    :param cols: the list of columns 
    
    :return: a tuple of stamp names
    """
    # create the stamp choices
    command = "gum choose"
    stamps = set()
    for col in cols:
        stamps.add(col.split()[0])

    for stamp in stamps:
        command += f' "{stamp}"'

    print("center stamp")
    center_stamp = prompt(command).lower()
    print("right stamp")
    right_stamp  = prompt(command).lower()
    print("left stamp")
    left_stamp   = prompt(command).lower()

    return center_stamp, right_stamp, left_stamp


def stamps_from_motion(motion):
    """
    Given the name of a motion, returns the tuple of stamps needed to calculate
    the angle of the motion
    
    :param motion: the motion name to get stamps for
    
    :return: the tuple of stamps needed to calculate the angle of the motion
    """
    motion = motion.lower()
    dict = {
        "chestaa":("shoulder", "hand"),
        "shoulderfe":("shoulder", "hand"),
        "shoulderaa":("shoulder", "hand"),
        "bicepc":("elbow", "shoulder", "hand"),
        "fingerp":("hand", "thumb", "index"),
        "bodylean": ("back", "neck", "leg"),
    }
    return dict[motion]


def columns_from_stamps(stamps, cols):
    """
    Given a tuple of stamps, and the columns of the dataset, returns the list
    of column names corresponding to the x and y of each stamp
    
    :param stamps: the tuple of stamps 
    :param cols: the list of data column names
    
    :return: a tuple of the columns corresponding to the given stamps
    """
    data = [None] * range(2*len(stamps))
    for col in cols:
        colwords = col.lower().split()
        for i in range(len(stamps)):
            if stamps[i] in colwords and 'x' in colwords:
                data[2*i] = col
            if stamps[i] in colwords and 'y' in colwords:
                data[2*i + 1] = col

    return tuple(data)


def main():
    chosen_file = prompt("gum file")

    # create pandas database
    df = pd.read_csv(chosen_file)

    # select stamps to do angle calculation with
    if "-p" in sys.argv:
        stamps = prompt_for_stamps(df.columns)
    else:
        motion = chosen_file.split("/")[-1].split(".")[0]
        stamps = stamps_from_motion(motion)

    # get database column names corresponding to stamps
    columns = columns_from_stamps(stamps, df.columns)
    print(chosen_file)
    print(stamps)
    print(df.columns)
    print(columns)



main()


# plot the graph
# df.plot(x=x_choice, y=y_choice, kind=graph_choice)
# plt.show()


