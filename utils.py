import os
import numpy as np

def pretty(str):
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
             "moca": "MOCA",
             "biostamp": "BioStamp",
             }
    if str in names:
        return names[str]
    else:
        return str.title()

def offset(s1,s2, offset):
    if offset >= 0:
        s1 = s1.iloc[offset:].reset_index(drop=True)
        s2 = s2.iloc[:len(s1)]
    else:
        s2 = s2.iloc[-offset:].reset_index(drop=True)
        s1 = s1.iloc[:len(s2)]
    return s1, s2


def maximize(fun,min,max):
    max = -100
    max_pos = 0
    for i in range(min,max):
        val = fun(i)
        if val > max:
            max = val
            max_pos = i
    return max, max_pos


def filter_for_terms(strs, *terms):
    """
    Filters the given list of strings based on the terms given.
    Is case-insensitive. If a term begins with `!`, the search 
    is inversed such that any items with that term are excluded.

    :return: a list of any strings that match all terms
    """

    terms = [t.lower() for t in terms]
    def match_fun(x): 
        x = x.lower()
        neg_terms = [term for term in terms if term[0] == '!']
        switch_terms = [term for term in terms if '|' in term]
        pos_terms = [term for term in terms if term not in switch_terms and term not in neg_terms]
        for term in pos_terms:
            if term not in x:
                return False
        for term in neg_terms:
            if term in x:
                return False
        for term in switch_terms:
            l = term.split('|')
            l = map(lambda t: t in x, l)
            if True not in l:
                return False

        return True

    return list(filter(match_fun, strs))

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

