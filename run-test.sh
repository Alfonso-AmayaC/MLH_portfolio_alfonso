#!/bin/bash

if [[ "$OSTYPE" == "msys" ]]; then
    $PWD/python3-virtualenv/Scripts/python -m unittest discover -v tests/
else
    $PWD/python3-virtualenv/bin/python -m unittest discover -v tests/
fi
