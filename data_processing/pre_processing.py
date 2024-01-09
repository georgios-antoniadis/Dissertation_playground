import pandas as pd
import os
# Config files
from configparser import ConfigParser
from datetime import datetime

def get_file_from_uploads(file_name):
    #Update config file
    config_object = ConfigParser()
    config_object.read("config.ini")
    #Get the SINGLESCOREINFO section
    config = config_object["USERFILE"]
    # request.form works with the elements' names 
    uploaded_file_path = config['file_path']

    return uploaded_file_path

def timestamp_check(filepath):
    df = pd.read_csv(filepath)

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%y %H:%M")
        return True
    except:
        print('Timestamp column cannot be transformed to datetime object')
        return False


def date_check(filepath):
    df = pd.read_csv(filepath)

    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%y %H:%M")

    current_date = datetime.now()

    print(df['timestamp'].max())

    if current_date < df['timestamp'].max():
        return False
    else:
        return True


def confirm_dataset_structure(uploaded_file_path):
    file_df = pd.read_csv(uploaded_file_path)
    flag = False
    if [file_df.columns[0],file_df.columns[1]] == ['timestamp', 'target']:
        flag = True
    else:
        flag = False
    
    return flag

def number_of_rows(uploaded_file_path):
    file_df = pd.read_csv(uploaded_file_path)
    flag = False
    if file_df.shape[0] > 10 and file_df.shape[0] < 10000:
        flag = True
    else:
        flag = False
    
    return flag

def pre_processing(file_name):

    uploaded_file = get_file_from_uploads(file_name)

    str_to_return = True

    if not confirm_dataset_structure(uploaded_file):
        str_to_return = 'Invalid column names! Expected column names "timestamp", "target"'
    elif not timestamp_check(uploaded_file):
        str_to_return =  'Invalid timestamp format! Expected column names "%d-%m-%y %H:%M"'
    elif not date_check(uploaded_file):
        str_to_return = 'Error: Some timestamps in dataset are in the future!'
    elif not number_of_rows(uploaded_file):
        str_to_return = 'Error: Dataset has either less than 10 rows or more than 10000!'

    if str_to_return == True:

        # ALL FILE PATHS MUST BE MADE WITH REFERENCE TO THEIR RELATIVE PATH COMPARED TO APP.PY

        config_object = ConfigParser()
        config_object.read("config.ini")
        
        # open_file = open('evaluation_protocol/test.txt','w')
        # print(open_file.readline())
        # open_file.close()

        print(config_object.sections())

        #Get the PREPROCESSING section
        config = config_object["PREPROCESSING"]

        config['passed'] = 'true'

        #Write changes back to file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)
    
    return str_to_return