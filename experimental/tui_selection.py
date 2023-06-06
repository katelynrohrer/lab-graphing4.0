import os
import sys
import platform
if platform.system() == 'Windows':
    import windows_curses as curses
else:
    import curses


def make_selection_menu(stdscr,opts):
    sel_index = 0
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    while True:
        stdscr.erase()

        for i, opt in enumerate(opts):
            if i == sel_index:
                stdscr.addstr(i+2, 0, f"> {opt}", curses.A_REVERSE)
            else:
                stdscr.addstr(i+2, 0, f"  {opt}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            sel_index = max(sel_index - 1, 0)
        elif key == curses.KEY_DOWN or key == ord('j'):
            sel_index = min(sel_index + 1, len(opts) - 1)
        elif key == curses.KEY_RIGHT or key == ord('l') or key == ord('\n'):
            selected_opt = opts[sel_index]
            break
        elif key == ord('q'):
            selected_opt = None
            break

    curses.curs_set(1)
    curses.endwin()

    return selected_opt



def make_file_menu(stdscr):
    # Set up initial variables
    current_dir = os.getcwd()
    file_list = os.listdir(current_dir)
    file_index = 0
    selected_file = None

    # Set up the curses screen
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()  # Enable color support
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)  # Define a color pair for directories
    stdscr.clear()

    while True:
        # Clear the screen
        stdscr.erase()

        # Print the current directory and file list
        stdscr.addstr(0, 0, f"Current directory: {current_dir}")
        dirs = []
        files = []
        for f in file_list: 
            (dirs if os.path.isdir(os.path.join(current_dir,f)) else files).append(f)
        file_list = sorted(dirs) + sorted(files)
        for i, file_name in enumerate(file_list):
            if i == file_index:
                stdscr.addstr(i+2, 0, f"> {file_name}", curses.A_REVERSE)
            else:
                if os.path.isdir(os.path.join(current_dir, file_name)):
                    stdscr.addstr(i+2, 0, f"  {file_name}", curses.color_pair(1))
                else:
                    stdscr.addstr(i+2, 0, f"  {file_name}")

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            file_index = max(file_index - 1, 0)
        elif key == curses.KEY_DOWN or key == ord('j'):
            file_index = min(file_index + 1, len(file_list) - 1)
        elif key == curses.KEY_RIGHT or key == ord('l'):
            selected_file = os.path.join(current_dir, file_list[file_index])
            if os.path.isdir(selected_file):
                current_dir = selected_file
                file_list = os.listdir(current_dir)
                file_index = 0
            else:
                break
        elif key == curses.KEY_LEFT or key == ord('h'):
            current_dir = os.path.dirname(current_dir)
            file_list = os.listdir(current_dir)
            file_index = 0
        elif key == ord('\n'):
            selected_file = os.path.join(current_dir, file_list[file_index])
            if os.path.isdir(selected_file):
                current_dir = selected_file
                file_list = os.listdir(current_dir)
                file_index = 0
            else:
                break
        elif key == ord('q'):
            selected_file = None
            break

    # Clean up the curses screen
    curses.curs_set(1)  # Show the cursor
    curses.endwin()

    # return the selected file path
    return selected_file

def select_file():
    return curses.wrapper(make_file_menu)

def select(opts):
    return curses.wrapper(lambda x: make_selection_menu(x, opts))

