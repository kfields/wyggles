# Wyggles :bug:

## Install

This package requires Cairo.  Either enter this on Ubuntu or visit https://www.cairographics.org/download/

        sudo apt install libcairo2-dev pkg-config python3-dev

Navigate to a directory where you keep your software projects

        cd projects

Clone the repository

        git clone https://github.com/kfields/wyggles.git
        
Change to the new directory which contains the repository

        cd wyggles

Create a Python 3 virtual environment called `env`

        python3 -m venv env
        
Activate the environment

        source env/bin/activate
        
Install required packages

        pip install -r requirements.txt

## Run
        python main.py
