#!/bin/sh

alias large_echo='{ set +x; } 2> /dev/null; f(){ echo "#\n#\n# $1\n#\n#"; set -x; }; f'

large_echo "Check OpenSSL installation path"
if brew ls --versions openssl > /dev/null; then
    OPENSSL_ROOT="$(brew --prefix openssl)"
    echo $OPENSSL_ROOT
else
    echo "Please install OpenSSL with brew: 'brew install openssl'"
    exit 1
fi

large_echo "Get the current working directory path"
CURRENT_DIR="$PWD"
echo $CURRENT_DIR

large_echo "Download source"
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
tar -zxvf Python-3.6.5.tgz &> /dev/null

large_echo "Build Python"
cd Python-3.6.5
./configure MACOSX_DEPLOYMENT_TARGET=10.9 CPPFLAGS="-I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib" --prefix="$CURRENT_DIR/python-portable"
make altinstall
