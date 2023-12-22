import pandas as pd
import os
# Config files
from configparser import ConfigParser

def get_file_from_uploads(file_name):
    uploaded_file_path = ''
    for file in os.listdir('uploads'):
        if ".csv" in file and file_name in file:
            print(f"Found uploaded file! {file}")
            uploaded_file_path = os.path.join('uploads',file)
            continue
    
    if confirm_dataset_structure(uploaded_file_path):
        print("File can be used")
    else:
        uploaded_file_path == 'File does not contain the correct columns'

    return uploaded_file_path

def timestamp_check(filepath):
    df = pd.read_csv(filepath)

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%y %H:%M")
        return True
    except:
        print('Timestamp column cannot be transformed to datetime object')
        return False


def confirm_dataset_structure(uploaded_file_path):
    file_df = pd.read_csv(uploaded_file_path)
    flag = False
    print(file_df.columns)
    if [file_df.columns[0],file_df.columns[1]] == ['timestamp', 'target']:
        flag = True
    else:
        flag = False
    
    return flag

def pre_processing(file_name):

    uploaded_file = get_file_from_uploads(file_name)

    str_to_return = True

    if not confirm_dataset_structure(uploaded_file):
        str_to_return = 'Invalid column names! Expected column names Timestamp, target'
    elif not timestamp_check(uploaded_file):
        str_to_return =  'Invalid timestamp format! Expected column names "%d-%m-%y %H:%M"'
    
    if str_to_return == True:

        # ALL FILE PATHS MUST BE MADE WITH REFERENCE TO THEIR RELATIVE PATH COMPARED TO APP.PY

        config_object = ConfigParser()
        config_object.read("evaluation_protocol/config.ini")
        
        # open_file = open('evaluation_protocol/test.txt','w')
        # print(open_file.readline())
        # open_file.close()

        print(config_object.sections())

        #Get the PREPROCESSING section
        config = config_object["PREPROCESSING"]

        config['passed'] = 'true'

        #Write changes back to file
        with open('evaluation_protocol/config.ini', 'w') as conf:
            config_object.write(conf)
    
    return str_to_return