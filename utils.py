import os

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

