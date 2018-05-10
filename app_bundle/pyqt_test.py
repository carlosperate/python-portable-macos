#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The code below has been adapted from the PyInstaller tests:
# https://github.com/pyinstaller/pyinstaller/blob/a70b20e4de6a6817987d28ca9f3201c8105fd858/tests/old_suite/interactive/test_pyqt5.py
#
# PyInstaller License file can be found in:
# https://github.com/pyinstaller/pyinstaller/blob/a70b20e4de6a6817987d28ca9f3201c8105fd858/COPYING.txt
#
#-----------------------------------------------------------------------------
# Copyright (c) 2013-2017, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import sys

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


def main():
    print("Python sys.executable:\n\t%s" % sys.executable)
    print("Python sys.path:\n\t%s" % "\n\t".join(sys.path))
    print('Qt5 Libraries path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.LibrariesPath))
    print('Qt5 Library Executables path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.LibraryExecutablesPath))
    print('Qt5 Binaries path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath))
    print('Qt5 Data path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.DataPath))
    print('Qt5 Imports path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.ImportsPath))
    print('Qt5 Plugins path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath))
    print('Qt5 Settings path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.SettingsPath))
    print('Qt5 Prefix path:\n\t%s' % \
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PrefixPath))
    print("Qt5 image read support:\n\t%s" % ', '.join([str(format).lower() \
        for format in QtGui.QImageReader.supportedImageFormats()]))

    app = QtWidgets.QApplication(sys.argv)
    print("Qt5 app.libraryPaths():\n\t%s" % "\n\t".join((app.libraryPaths())))
    label = QtWidgets.QLabel("Hello World from PyQt5", None)
    label.setWindowTitle("Hello World from PyQt5")
    label.resize(300, 300)
    label.show()
    app.exec_()


if __name__ == "__main__":
    main()