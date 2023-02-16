"""
    File: export_graphs.py
    Purpose: exports the graphs for MOCA csv
    Known bugs: none at the moment.
"""
import glob
import os
from graph_single import *

"""
File tings for katie
    current_dir = os.getcwd()
    parent_dir = current_dir[:current_dir.rindex(os.sep)]
    abs_path = os.path.abspath("")[:os.path.abspath("").rindex(os.sep)]

    (was on line 51 or something)"all_images", motion, subject,
"""

def find_files(search_dir, search_term=""):
    """
    globs the associated MOCA csv files from the given search directory.
    you can also specify the search term (which can be anything)

    :param search_dir: the directory to search from
    :param search_term: (optional) a given search term that can come before 
        the file extension for a given file

    :return: the files in a list
    """
    csv_path = os.path.join(search_dir, "Lab")
    files = glob.glob(csv_path + os.sep + "**" + \
            os.sep + f"*{search_term}*angularDisp.csv", recursive=True)
    return files

def export(chosen_file, dest_dir):
    """
    Exports the chosen files to the destination directory. 
    note that the file names are identical to the csv file that they originate
    from and exported as pngs.

    :param chosen_file: the chosen filepath to export
    :param dest_dir: the destination directory to export the file to 

    :return: None
    """
    csv_file_name = chosen_file[chosen_file.rindex(os.sep)+1:-4]
    file_info = csv_file_name.split(".")
    file_info = [item for item in file_info if item != ""]
    motion = file_info[0].lower()
    subject = file_info[2].lower()

    save_file_name = csv_file_name + ".png"

    save_path = os.path.join(dest_dir,  save_file_name)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.5)

def main():
    # the search directory might be different from the destination directory
    # your search directry depends entirely on where 'All-Lab-Data' exists 
    search_dir = "/Users/melancwaly/code/All-Lab-Data"
    destination_dir = "/Users/melancwaly/code/All-Lab-Data/all_images/angularDisp"
    files = find_files(search_dir)

    for file in files:
        print(f"processing file: {file}")
        graph_single(file)
        export(file, destination_dir)

if __name__ == "__main__":
    main()
