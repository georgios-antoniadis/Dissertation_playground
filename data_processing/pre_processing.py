import pandas as pd
import os

def get_file_from_uploads():
    uploaded_file_path = ''
    for file in os.listdir('uploads'):
        if ".csv" in file:
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

def pre_processing():

    uploaded_file = get_file_from_uploads()

    str_to_return = True

    if not confirm_dataset_structure(uploaded_file):
        str_to_return = 'Invalid column names! Expected column names Timestamp, target'
    elif not timestamp_check(uploaded_file):
        str_to_return =  'Invalid timestamp format! Expected column names "%d-%m-%y %H:%M"'
    
    return str_to_return