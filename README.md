# Dissertation
Traditional vs Machine Learning methods for timeseries forecasting

# Setup
It is recommended that you setup a python virtual environment in your system and run the application from inside it.

## Creating a virtual environment: (Linux - Ubuntu)
1) sudo apt install python3.8-venv
2) python3 -m venv dissertation_venv
3) source dissertation_venv/bin/activate

## Installing required packages
Once incide the virtual environment:
1) pip install -r requirements.txt

## Running the application
1) Open an interactive terminal
2) python app.py
3) Access the URL printed from a browser

# Dependencies
The application requires all libraries from requirements.txt to be installed in the virtual python environment

# Referencing inside the application
The main application initializes by executing app.py
All other componenets are called as modules from app.py and to function properly all paths inside them should be declared as if they were referenced from the parent folder of the project (the directory containing app.py)
e.g. For config.ini which is in the same directory as app.py, if we were to declare its relative path inside a module from "data_processing" we would still declare it as "config.ini" rather than "../config.ini"