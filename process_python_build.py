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


# Python version is used for folder names and exec files in built output
PYTHON_VER = 'python3.6'

# Safe directories we can remove from a Python build folder
PYTHON_REMOVE_DIRS = [
    os.path.join('lib', PYTHON_VER, 'ensurepip'),
    os.path.join('lib', PYTHON_VER, 'idlelib'),
    os.path.join('lib', PYTHON_VER, 'test'),
]


def remove_file(file_to_remove):
    if os.path.isfile(file_to_remove):
        print('Removing file {}'.format(file_to_remove))
        os.remove(file_to_remove)
    else:
        print('File {} was not found.'.format(file_to_remove))


def remove_directory(dir_to_remove):
    """
    Removes the given directory if it exists, print info out if not.
    :param dir_to_remove: Path to folder to remove.
    """
    if os.path.isdir(dir_to_remove):
        print('Removing directory {}'.format(dir_to_remove))
        shutil.rmtree(dir_to_remove)
    else:
        print('Directory {} was not found.'.format(dir_to_remove))


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

    print('Compiling file {} to {}'.format(py_file, pyc_file))
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
            print(msg + ' will be used as python path:\n\t{}'.format(abs_path))
            return abs_path
        else:
            raise Exception(msg + ', but it is not a valid path')
    else:
        raise Exception('No command line argument found')


def compress_folder(folder_path, zip_file_path, zip_as_folder=True):
    """
    Compresses the folder indicated by folder_path, without the a pa
    """
    folder_path = os.path.abspath(folder_path)
    zip_file_path = os.path.abspath(zip_file_path)
    if os.path.isfile(zip_file_path):
        raise Exception('Destination file {} already exists.'.format(
                zip_file_path))

    old_cwd = os.getcwd()
    parent_path = os.path.dirname(folder_path)
    if zip_as_folder:
        os.chdir(parent_path)
        zip_folder = os.path.relpath(folder_path, parent_path)
    else:
        os.chdir(folder_path)
        zip_folder = '.'

    zip_process = subprocess.Popen(
            ["zip", "--symlinks", "-r", zip_file_path, zip_folder],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    std_out, std_err = zip_process.communicate()
    if std_err:
        raise Exception('Error zipping standard library:\n{}'.format(std_err))

    os.chdir(old_cwd)


def main(args):
    python_path = get_python_path(args)
    std_lib_path = os.path.join(python_path, 'lib', PYTHON_VER)
    python_exec_path = os.path.join(python_path, 'bin', PYTHON_VER)

    print('\nRemove unnecessary directories:')
    for dir_ in PYTHON_REMOVE_DIRS:
        remove_directory(os.path.join(python_path, dir_))

    print('\nRemove __pycache__ directories from "{}"'.format(std_lib_path))
    remove_pycache_dirs(std_lib_path)

    print('\nCompile Python files from "{}"'.format(std_lib_path))
    compile_pyc_dir(python_exec_path, std_lib_path)

    print('\nRemove Python source files from "{}"'.format(std_lib_path))
    remove_file_type_from('py', std_lib_path)

    print('\nRemove __pycache__ directories from "{}"'.format(std_lib_path))
    remove_pycache_dirs(std_lib_path)

    # TODO: Figure out compressing issue and if it's worth doing
    # print('\nCompressing the stand library "{}"'.format(std_lib_path))
    # compress_folder(std_lib_path,
    #                 os.path.join(python_path, 'lib', PYTHON_VER + '.zip'),
    #                 zip_as_folder=False)
    # print('\nRemove uncompressed stand library dir"{}"'.format(std_lib_path))
    # remove_directory(std_lib_path)

    print('All done! :)')



if __name__ == "__main__":
    main(sys.argv[1:])
