#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Moves required files into a macOS/OS X app bundle directory.
"""
import os
import sys
import shutil
import subprocess


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
    if std_err:
        raise Exception('Error zipping standard library:\n{}'.format(std_err))

    os.chdir(old_cwd)


def make_executable(path):
    """
    From: https://stackoverflow.com/questions/12791997/
    """
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


def create_app_bundle(bundle_dir, bundle_name, python_dir):
    old_cwd = os.getcwd()
    os.chdir(bundle_dir)
    app_bundle_name = bundle_name + '.app'
    if os.path.exists(app_bundle_name):
        raise Exception('App bundle with name {} already exists in:'
                        '\n{}'.format(app_bundle_name, bundle_dir))

    help_files = get_project_app_bundle_path()

    # Create all the App Bundle required folders
    print('\tCreating the App Bundle folders required...')
    os.makedirs(app_bundle_name)
    contents_dir = os.path.join(app_bundle_name, 'Contents')
    os.makedirs(contents_dir)
    frameworks_dir = os.path.join(contents_dir, 'Frameworks')
    os.makedirs(frameworks_dir)
    macos_dir = os.path.join(contents_dir, 'MacOS')
    os.makedirs(macos_dir)
    resources_dir = os.path.join(contents_dir, 'Resources')
    os.makedirs(resources_dir)

    # Copy Info.plist into top of Contents
    print('\tAdding Info.plist...')
    origin_info_plist = os.path.join(help_files, 'Info.plist')
    destination_info_plist = os.path.join(contents_dir, 'Info.plist')
    shutil.copyfile(origin_info_plist, destination_info_plist)

    # Copy the icon into the Resources folder
    print('\tAdding app icon...')
    origin_icon = os.path.join(help_files, 'appIcon.icns')
    destination_icon = os.path.join(resources_dir, 'appIcon.icns')
    shutil.copyfile(origin_icon, destination_icon)

    # Copy python_dir to the Resources folder
    print('\tCopy the Python folder...')
    py_folder_name = os.path.basename(python_dir)
    destination_python = os.path.join(resources_dir, py_folder_name)
    shutil.copytree(python_dir, destination_python)

    # Copy test file to the Resources folder
    print('\tAdd a luncher Python file for testing PyQt hello world...')
    origin_py_file = os.path.join(help_files, 'pyqt_test.py')
    destination_py_file = os.path.join(resources_dir, 'pyqt_test.py')
    shutil.copyfile(origin_py_file, destination_py_file)

    # Copy shell script to the MacOS folder and set it executable
    print('\tAdd internal executable...')
    origin_sh_file = os.path.join(help_files, 'run.sh')
    destination_sh_file = os.path.join(macos_dir, bundle_name)
    shutil.copyfile(origin_sh_file, destination_sh_file)
    make_executable(destination_sh_file)

    os.chdir(old_cwd)


def get_project_app_bundle_path():
    """
    There is a folder called "app_bundle" in the same directory as this file.
    """
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'app_bundle')


def parse_args(args):
    """
    We expect the following command line arguments in the following order:
        <path to python portable directory>
        <name of bundle app>
    """
    py_path = None
    bundle_name = None
    if len(args) == 2:
        msg = 'Command line argument "{}" found'.format(args[0])
        # Take the first argument and use it as a tag appendage
        if os.path.isdir(args[0]):
            py_path = os.path.abspath(args[0])
            print(msg + ' will be used as python path:\n\t{}'.format(py_path))
        else:
            raise Exception(msg + ', but it is not a valid path')
        bundle_name = args[1]
        print('"{}" name will be used for the app bundle'.format(bundle_name))
    else:
        raise Exception('Did not find the right number of command line '
                        'arguments. Found {} arguments'.format(len(args)))
    return py_path, bundle_name


def main(args):
    python_dir, bundle_name = parse_args(args)

    print('Creating the App Bundle for "{}" app:'.format(bundle_name))
    create_app_bundle(bundle_dir=os.getcwd(),
                      bundle_name=bundle_name,
                      python_dir=python_dir)

    print('Compressing the "{}" App Bundle'.format(bundle_name))
    compress_folder(folder_path='{}.app'.format(bundle_name),
                    zip_path='{}-portable.zip'.format(bundle_name.lower()),
                    zip_as_folder=True)

    print('All done! :)')


if __name__ == "__main__":
    main(sys.argv[1:])
