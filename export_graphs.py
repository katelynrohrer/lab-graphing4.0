
import glob
import os
from graph_single import *


def main():
    files = find_files()
    for file in files:
        graph_single(file)
        export(file)

def find_files(search_term=""):
    current_dir = os.getcwd()
    parent_dir = current_dir[:current_dir.rindex(os.sep)]
    csv_path = os.path.join(parent_dir, "All-Lab-Data", "Lab")
    files = glob.glob(csv_path + os.sep + "**" + os.sep + f"*{search_term}*angularDisp.csv", recursive=True)
    return files

def export(chosen_file):
    csv_file_name = chosen_file[chosen_file.rindex(os.sep)+1:-4]
    file_info = csv_file_name.split(".")
    file_info = [item for item in file_info if item != ""]
    motion = file_info[0].lower()
    subject = file_info[2].lower()

    save_file_name = csv_file_name + ".png"


    abs_path = os.path.abspath("")[:os.path.abspath("").rindex(os.sep)]
    save_path = os.path.join(abs_path, "All-Lab-Data", "all_images", motion, subject, save_file_name)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.5)

if __name__ == "__main__":
    main()
