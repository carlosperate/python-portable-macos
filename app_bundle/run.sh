#!/bin/bash

# Get the directory where this file is located and App Bundle Resources
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
RESOURCES_DIR="$(dirname "$DIR")/Resources"
echo $RESOURCES_DIR

# Add to the top of Path the Python bin
PATH="$RESOURCES_DIR/python-portable/bin/:$PATH"

#"$RESOURCES_DIR/python-portable/bin/python3.6" -m mu
"$RESOURCES_DIR/python-portable/bin/python3.6" "$RESOURCES_DIR/pyqt_test.py"
