#!/bin/bash

PYPI_IDX=

# set -x

# check user input
if [[ -z $1 ]] || { [[ $1 != "client" ]] && [[ $1 != "server" ]]; }; then
    echo "Usage:"
    echo "./install.sh [client|server] [venv]"
    exit
fi

# check env setup
if python3 -V; then
    py=python3
else
    py_ver=$(python -c 'import sys; print(sys.version_info.major)')
    if [[ ! py_ver -eq 3 ]]; then
        echo "Python3 only"
        exit
    fi
    py=python
fi

if [[ $2 == "venv" ]]; then
    sudo apt update
    sudo apt install python3-virtualenv -y

    $py -m venv venv

    source venv/bin/activate
    py=venv/bin/python
else
    py=python
fi

$py -m pip install -U pip $PYPI_IDX

if [[ $1 == "server" ]]; then
    $py -m pip install flask $PYPI_IDX
elif [[ $1 == "client" ]]; then
    $py -m pip install requests $PYPI_IDX
fi

echo "Setup complete"
