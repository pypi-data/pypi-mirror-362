import os
from tkinter import filedialog
from tkinter import Tk as _Tk
import shutil
import gzip


def find_files(folder, extension=""):
    """
    =============================
    File Finder Utility
    =============================

    This function searches for files with a specific extension within a given folder and its subdirectories.

    :param folder: The root directory to start the search.
    :type folder: str
    :param extension: The file extension to search for. If empty, all files are returned.
    :type extension: str, `optional`

    :returns: A list of file paths that match the specified extension.
    :rtype: list

    **Example Usage**
    -----------------
    .. code-block:: python

        result = find_files('/path/to/folder', '.txt')
        print(result)  # ['/path/to/folder/file1.txt', '/path/to/folder/subfolder/file2.txt']

    **See Also**
    ------------
    - `os.walk <https://docs.python.org/3/library/os.html#os.walk>`_
    """
    all_files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(extension):
                all_files.append(os.path.join(dirpath, filename))
    return all_files


def select_files(max_files=None, single_file_mode=False):
    """
    =============================
    File Selection Utility
    =============================
    Opens a file dialog for the user to select one or more files, with optional limits on the number of files.

    :param max_files: The maximum number of files the user is allowed to select. If None, no limit is enforced.
    :type max_files: int or None

    :param single_file_mode: If True, only a single file can be selected. Overrides max_files if set.
    :type single_file_mode: bool

    :returns: A list of selected file paths.
    :rtype: list

    **Example Usage**
    -----------------
    .. code-block:: python
        selected_files = select_files(max_files=2)
        print(selected_files)  # ['/path/to/file1', '/path/to/file2']
    **See Also**
    ------------
    - `tkinter.filedialog.askopenfilenames <https://docs.python.org/3/library/tkinter.filedialog.html#tkinter.filedialog.askopenfilenames>`_
    - `tkinter.filedialog.askopenfilename <https://docs.python.org/3/library/tkinter.filedialog.html#tkinter.filedialog.askopenfilename>`_
    """

    # Hide the main tkinter window
    root = _Tk()
    root.withdraw()

    # If single file mode is enabled, use askopenfilename instead
    if single_file_mode or max_files == 1:
        selected_files = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    else:
        # Open the file dialog
        selected_files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("All files", "*.*")],
        )
    # check if max_files is specified and if exceeded let he user know in a message box
    if max_files is not None and len(selected_files) > max_files:
        from tkinter import messagebox

        messagebox.showerror("Error", f"Please select a maximum of {max_files} files.")
        root.destroy()
        return select_files(max_files=max_files, single_file_mode=single_file_mode)

    # If cancel is pressed, quit the program
    if not selected_files:
        exit()
    # Return the list of selected files
    return list(selected_files)


def remove_files(folder, extension=""):
    """
    =============================
    File Removal Utility
    =============================

    This function removes files with a specific extension from a given folder.

    :param folder: The path to the folder from which files will be removed.
    :type folder: str
    :param extension: The file extension to filter files for removal. If empty, all files will be removed.
    :type extension: str, `optional`

    :returns: None
    :rtype: None

    **Example Usage**
    -----------------
    .. code-block:: python

        remove_files('/path/to/folder', '.txt')

    **See Also**
    ------------
    - `os.listdir <https://docs.python.org/3/library/os.html#os.listdir>`_
    - `os.remove <https://docs.python.org/3/library/os.html#os.remove>`_
    """
    for file in os.listdir(folder):
        if file.endswith(extension):
            os.remove(os.path.join(folder, file))


def get_txt_lines(txt_file):
    """
    ===========================
    Text File Lines Extraction
    ===========================

    This function reads a text file and returns its lines as a list of strings, with each line stripped of leading and trailing whitespace.

    :param txt_file: The path to the text file to read.
    :type txt_file: str

    :returns: A list of strings, each representing a line from the text file.
    :rtype: list

    **Example Usage**
    -----------------
    .. code-block:: python

        lines = get_txt_lines("example.txt")
        print(lines)  # ['First line', 'Second line', 'Third line']

    **See Also**
    ------------
    - `Python File I/O <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>`_
    """
    lines = []
    with open(txt_file, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def copy_file(item, output_folder):
    """
    =============================
    File Copy Utility
    =============================

    This function copies a file to the specified output folder.

    :param item: The path to the file to be copied.
    :type item: str
    :param output_folder: The path to the folder where the file should be copied.
    :type output_folder: str

    :returns: None
    :rtype: None

    **Example Usage**
    -----------------
    .. code-block:: python

        copy_file('example.txt', '/path/to/output/folder')

    **See Also**
    ------------
    - `shutil.copy <https://docs.python.org/3/library/shutil.html#shutil.copy>`_
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    shutil.copy(item, output_folder)


def zip_files(directory):
    """
    =============================
    File Zipping Utility
    =============================
    This function compresses files in a given directory into gzip format.

    :param directory: The directory containing files to be compressed.
    :type directory: str

    :returns: None

    **Example Usage**
    -----------------
    .. code-block:: python
        zip_files('/path/to/directory')

    **See Also**
    ------------
    - `gzip module documentation <https://docs.python.org/3/library/gzip.html>`_
    """
    for file in find_files(directory):
        with open(file, "rb") as f:
            content = f.read()

        # Get the relative path of the file from the input directory
        relative_path = os.path.relpath(file, directory)

        # Create the output directory structure
        output_dir = os.path.join("output", os.path.dirname(relative_path))
        os.makedirs(output_dir, exist_ok=True)

        # Create the output file path without the .html extension
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file))[0] + ".gz")

        with gzip.open(output_file, "wb") as f:
            f.write(content)


def move_files(source_folder, destination_folder, extension=""):
    """
    =============================
    File Moving Utility
    =============================

    This function moves files from a source folder to a destination folder, optionally filtering by file extension.

    :param source_folder: The folder to move files from.
    :type source_folder: str
    :param destination_folder: The folder to move files to.
    :type destination_folder: str
    :param extension: The file extension to filter by. Only files with this extension will be moved. If empty, all files will be moved.
    :type extension: str, `optional`

    :returns: None
    :rtype: None

    **Example Usage**
    -----------------
    .. code-block:: python

        move_files('/path/to/source', '/path/to/destination', '.txt')

    **See Also**
    ------------
    - `shutil.move <https://docs.python.org/3/library/shutil.html#shutil.move>`_
    - `os.makedirs <https://docs.python.org/3/library/os.html#os.makedirs>`_
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file in os.listdir(source_folder):
        if file.endswith(extension):
            shutil.move(os.path.join(source_folder, file), destination_folder)


def merge_text_files(file_list, output_file):
    """
    ===========================
    Merge Text Files Utility
    ===========================

    This function merges multiple text files into a single output file.

    :param file_list: A list of file paths to be merged.
    :type file_list: list of str
    :param output_file: The path to the output file where the merged content will be written.
    :type output_file: str

    :returns: None

    **Example Usage**
    -----------------
    .. code-block:: python

        file_list = ["file1.txt", "file2.txt", "file3.txt"]
        output_file = "merged_output.txt"
        merge_text_files(file_list, output_file)

    **See Also**
    ------------
    - `File Handling in Python <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>`_
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file in file_list:
            with open(file, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")


def write_list_to_file(list_of_lines, file_path):
    """
    =============================
    File Writing Utility
    =============================

    This function writes a list of lines to a specified file.

    :param list_of_lines: The list of lines to write to the file.
    :type list_of_lines: list
    :param file_path: The path to the file where the lines will be written.
    :type file_path: str

    :returns: None
    :rtype: None

    **Example Usage**
    -----------------
    .. code-block:: python

        lines = ["First line", "Second line", "Third line"]
        write_list_to_file(lines, "/path/to/file.txt")

    **See Also**
    ------------
    - `Python File I/O <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>`_
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for line in list_of_lines:
            f.write(str(line) + "\n")


def remove_duplicate_lines(file_path, output_file):
    """
    =============================
    Remove Duplicate Lines Utility
    =============================

    This function removes duplicate lines from a file and writes the unique lines to an output file.

    :param file_path: The path to the input file containing lines to be processed.
    :type file_path: str
    :param output_file: The path to the output file where unique lines will be written.
    :type output_file: str

    :returns: None
    :rtype: None

    **Example Usage**
    -----------------
    .. code-block:: python

        remove_duplicate_lines("input.txt", "output.txt")

    **See Also**
    ------------
    - `File Handling in Python <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>`_
    """
    seen = set()
    with open(file_path, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            if line not in seen:
                f_out.write(line)
                seen.add(line)


def select_directory(title="Select Directory"):
    """
    =============================
    Directory Selection Utility
    =============================

    This function opens a dialog for the user to select a directory.

    :param title: The title of the directory selection dialog.
    :type title: str, `optional`

    :returns: The path of the selected directory.
    :rtype: str

    **Example Usage**
    -----------------
    .. code-block:: python

        directory = select_directory()
        print(directory)  # Outputs the path of the selected directory

    **See Also**
    ------------
    - `tkinter.filedialog.askdirectory <https://docs.python.org/3/library/tkinter.filedialog.html#tkinter.filedialog.askdirectory>`_
    """
    root = _Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title=title)
    if not directory:
        exit()
    return directory


def find_all_directory_files(extension=""):
    """
    =============================
    Directory File Finder Utility
    =============================

    Prompts the user to select a directory and returns a list of files within that directory (and its subdirectories)
    that match the specified extension.

    :param extension: The file extension to search for. If empty, all files are returned.
    :type extension: str, `optional`

    :returns: A list of file paths that match the specified extension.
    :rtype: list

    **Example Usage**
    -----------------
    .. code-block:: python

        files = find_all_directory_files('.py')
        print(files)  # ['/selected/dir/script1.py', '/selected/dir/subdir/script2.py']

    **See Also**
    ------------
    - `os.walk <https://docs.python.org/3/library/os.html#os.walk>`_
    - `tkinter.filedialog.askdirectory <https://docs.python.org/3/library/tkinter.filedialog.html#tkinter.filedialog.askdirectory>`_
    """
    dir = select_directory()
    files = find_files(dir, extension)
    return files
