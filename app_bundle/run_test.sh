#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

"$DIR/../Resources/python-portable/bin/python3.6" "$DIR/../Resources/test.py"
