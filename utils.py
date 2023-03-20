import os
import numpy as np

def find_offset(a, v):
    max_corr = -np.inf
    best_offset = 0

    # Loop over possible offsets between a and v
    for offset in range(len(a)):
        shifted_v = v[offset:] + v[:offset]  # shift v by the offset
        corr = np.corrcoef(a, shifted_v)[0, 1]  # compute correlation between a and shifted v
        
        if corr > max_corr:  # update max_corr and best_offset if corr is larger
            max_corr = corr
            best_offset = offset

    print("Best offset:", best_offset)
    print("Max correlation:", max_corr)


def abbrev(strings):
    """
    Given a collection of strings, creates a list of unique abbreviations for
    each one. Creates global variables for these abbreviations, and prints
    out the mapping.

    :param strings: collection of strings to abbreviate

    :return: dictionary mapping abbreviations to their corresponding strings
    """
    dict = {}
    for s in strings:
        abbrev = ""
        index = 1
        words = s.split()
        for word in words:
            word = "".join(filter(str.isalpha, word))
            abbrev += word[:index]
        while abbrev in dict:
            abbrev = ""
            index += 1
            for word in words:
                abbrev += word[:index]

        dict[abbrev] = s

    return dict

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

