# python-portable-macos

[![Build Status](https://travis-ci.org/carlosperate/python-portable-macos.svg?branch=master)](https://travis-ci.org/carlosperate/python-portable-macos)

An attempt to make a portable version of Python for macOS in order to pack Python applications into self-contained executables.

Includes scripts to build Python and package it into a Mac Application Bundle.

Travis CI is used to build and package it, output files are temporary stored (only for two weeks) in the wonderful https://transfer.sh service. To download individual commits you need to find the unique transfer.sh URL at the end of the Travis build log:

```bash
$ cat output_urls.txt
https://transfer.sh/K3Hef/python3-only.zip
https://transfer.sh/4wYXQ/python3-only-reduced.zip
https://transfer.sh/xuxaL/mu-portable.zip
https://transfer.sh/LOoqY/Mu-Installer.dmg

The command "cat output_urls.txt" exited with 0.
```


## Things to do/test

- [ ] See if the SSL module works well in other platforms (pip install should be a good test) that do not have any version of OpenSSL installed
- [ ] Figure out a good test suit for Python standard library
- [ ] Figure out more files that can be safely removed from the Python build to reduce size
- [ ] Figure out if pymalloc version (python3.6m) is worth using and/or safe with current Mu dependencies
- [ ] Test in older macOS versions than 10.13 High Sierra
- [ ] Test in 10.9 Mavericks (Compile flag for 10.9, Travis environment uses 10.10 Yosemite)
- [ ] Simple PyQt5 test works, Mu fails to open, likely an exception is raised, so need to investigate
- [ ] Create a background PNG image for the DMG folder
