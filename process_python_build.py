#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prepares a portable Python directory.
"""
import os
import sys
import shutil
import subprocess
import py_compile


VERBOSE = False

# Python version is used for folder names and exec files in built output
VERSION_STR = '3.6'
PYTHON_VER = 'python{}'.format(VERSION_STR)

# Set the files and directories we can remove from a Python build folder
PYTHON_REMOVE_DIRS = [
    os.path.join('share', 'man'),
    os.path.join('lib', PYTHON_VER, 'ensurepip'),
    os.path.join('lib', PYTHON_VER, 'idlelib'),
    os.path.join('lib', PYTHON_VER, 'test'),
]
PYTHON_REMOVE_FILES = [
    #os.path.join('lib', PYTHON_VER, 'ensurepip'),
    #os.path.join('bin', '{}m'.format(PYTHON_VER)),
]

# Files and folders to keep inside the bin folder
PYTHON_KEEP_BIN_ITEMS = [
    PYTHON_VER,
    'pip{}'.format(VERSION_STR),
]


def remove_file(file_to_remove):
    """
    Removes the given file if it exists, print info out if not.
    :param file_to_remove: Path to file to remove.
    """
    if os.path.isfile(file_to_remove):
        if VERBOSE:
            print('\tRemoving file {}'.format(file_to_remove))
        os.remove(file_to_remove)
    else:
        print('\tFile {} was not found.'.format(file_to_remove))


def remove_directory(dir_to_remove):
    """
    Removes the given directory if it exists, print info out if not.
    :param dir_to_remove: Path to folder to remove.
    """
    if os.path.isdir(dir_to_remove):
        if VERBOSE:
            print('\tRemoving directory {}'.format(dir_to_remove))
        shutil.rmtree(dir_to_remove)
    else:
        print('\tDirectory {} was not found.'.format(dir_to_remove))


def remove_file_type_from(file_extension, scan_path):
    """
    Goes through a directory recursively and removes all files with an specific
    extension.
    :param file_extension: File extension of the files to remove.
    :param scan_path: Directory to scan for file type removal.
    """
    for root, dirs, files in os.walk(scan_path, topdown=False):
        for file_ in files:
            if file_.endswith('.' + file_extension):
                file_path = os.path.join(root, file_)
                remove_file(file_path)


def remove_all_folder_items_except(items_to_exclude, scan_path):
    """
    Goes through a directory immediate child files and folders and remove all
    except those indicated in the items_to_exclude argument.
    The items_to_exclude list MUST NOT contain full paths, just file/folder
    names.
    """
    scan_path = os.path.abspath(scan_path)
    for entry_name in os.listdir(scan_path):
        full_path = os.path.join(scan_path, entry_name)
        if os.path.exists(full_path) and entry_name not in items_to_exclude:
            remove_file(full_path)


def compress_folder(folder_path, zip_path, zip_as_folder=True):
    """
    Compresses the folder indicated by folder_path, without the a pa
    """
    folder_path = os.path.abspath(folder_path)
    zip_path = os.path.abspath(zip_path)
    if os.path.isfile(zip_path):
        raise Exception('Destination file {} already exists.'.format(zip_path))

    old_cwd = os.getcwd()
    parent_path = os.path.dirname(folder_path)
    if zip_as_folder:
        os.chdir(parent_path)
        path_to_zip = os.path.relpath(folder_path, parent_path)
    else:
        os.chdir(folder_path)
        path_to_zip = '.'

    zip_process = subprocess.Popen(
            ["zip", "--symlinks", "-r", zip_path, path_to_zip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    std_out, std_err = zip_process.communicate()
    if VERBOSE:
        print(std_out)
    if std_err:
        raise Exception('Error zipping standard library:\n{}'.format(std_err))

    os.chdir(old_cwd)


def remove_pycache_dirs(scan_path):
    """
    Recursively removes all folders named "__pycache__" from the given path.
    :param scan_path: Directory to scan for __pycache__ removal.
    :return:
    """
    for root, dirs, files in os.walk(scan_path, topdown=False):
        for name in dirs:
            if name == '__pycache__':
                remove_directory(os.path.join(root, name))


def compile_pyc(py_file, pyc_file):
    """
    Uses current running interpreter, compiles a Python file into a pyc file.
    """
    py_file = os.path.abspath(py_file)
    pyc_file = os.path.abspath(pyc_file)

    if not os.path.isfile(py_file) or not py_file.lower().endswith('.py'):
        raise Exception('Not a Python source file: {}'.format(py_file))
    if os.path.isfile(pyc_file):
        raise Exception('Destination file {} already exists.'.format(pyc_file))

    print('\tCompiling file {} to {}'.format(py_file, pyc_file))
    py_compile.compile(py_file, cfile=pyc_file, doraise=True)


def compile_pyc_dir(python_exec_path, src_path):
    """
    Use the command line to execute compileall python utility on a directory.
    """
    py_process = subprocess.Popen(
            [python_exec_path, '-m', 'compileall', '-b', '-f', src_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    std_out, std_err = py_process.communicate()
    if VERBOSE:
        print(std_out)
    if std_err:
        raise Exception('Error using Python compileall:\n{}'.format(std_err))


def get_python_path(args):
    """
    Gets the first item of the args list and verifies is a valid path to a
    directory. Assumes the input argument comes from the command line.
    """
    # Check if a command line argument has been given
    if args:
        msg = 'Command line argument "{}" found'.format(args[0])
        # Take the first argument and use it as a tag appendage
        if os.path.isdir(args[0]):
            abs_path = os.path.abspath(args[0])
            print('{} as Python path:\n\t{}'.format(msg, abs_path))
            return abs_path
        else:
            raise Exception(msg + ', but it is not a valid path')
    else:
        raise Exception('No command line argument found')


def main(args):
    python_path = get_python_path(args)
    std_lib_path = os.path.join(python_path, 'lib', PYTHON_VER)
    bin_path = os.path.join(python_path, 'bin')
    python_exec_path = os.path.join(python_path, 'bin', PYTHON_VER)
    global VERBOSE

    print('Remove unnecessary directories:')
    VERBOSE = True
    for dir_ in PYTHON_REMOVE_DIRS:
        full_path = os.path.join(python_path, dir_)
        remove_directory(full_path)
    VERBOSE = False

    print('Remove unnecessary files:')
    VERBOSE = True
    for file_ in PYTHON_REMOVE_FILES:
        full_path = os.path.join(python_path, file_)
        print('\tRemoving "{}"'.format(full_path))
        remove_file(full_path)
    remove_all_folder_items_except(PYTHON_KEEP_BIN_ITEMS, bin_path)
    VERBOSE = False

    print('Remove __pycache__ directories from "{}"'.format(std_lib_path))
    remove_pycache_dirs(std_lib_path)

    print('Compile Python files from "{}"'.format(std_lib_path))
    compile_pyc_dir(python_exec_path=python_exec_path, src_path=std_lib_path)

    print('Remove Python source files from "{}"'.format(std_lib_path))
    remove_file_type_from('py', std_lib_path)

    print('Remove __pycache__ directories from "{}"'.format(std_lib_path))
    remove_pycache_dirs(std_lib_path)

    # TODO: Figure out compressing issue and if it's worth doing
    # print('\nCompressing the stand library "{}"'.format(std_lib_path))
    # compress_folder(std_lib_path,
    #                 os.path.join(python_path, 'lib', PYTHON_VER + '.zip'),
    #                 zip_as_folder=False)
    # print('\nRemove uncompressed stand library dir"{}"'.format(std_lib_path))
    # remove_directory(std_lib_path)

    print('\nAll done! :)')


if __name__ == "__main__":
    main(sys.argv[1:])
