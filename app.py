from flask import Flask, render_template, request, jsonify, render_template_string, send_from_directory
import os
from tkinter import *
import pandas as pd
import importlib
import time
from memory_profiler import profile, memory_usage
from datetime import date, datetime
# import filedialog module
from tkinter import filedialog
import shutil
from tabulate import tabulate

# My custom evaluation protocol
from evaluation_protocol.grubbs import grubbs_score
from evaluation_protocol.shape_similarity import dtw
from evaluation_protocol.result_string import eval_string
from evaluation_protocol.performance_metrics import rmse, nme, mae, mse, mape, smape
from evaluation_protocol.single_scoring import score

# Dataset
from data_processing.transform import create_df_with_datetimes
from data_processing.pre_processing import pre_processing

# Config files
from configparser import ConfigParser

app = Flask(__name__, static_url_path='/static', static_folder='static')
# CORS(app)

result = ''
export = 'This is the export file'

train_file = 'Dataset/Yearly-train.csv'
test_file = 'Dataset/Yearly-test.csv'


# CONTROLLER
###########################################################################
# Printing the evaluation protocol string
def scoring(predicted, real, method_type, method, elapsed_time_sec, complexity):
    if os.path.exists('session_file.csv'):
        session_file = open('session_file.csv', 'a')
    else:
        session_file = open('session_file.csv', 'w')
        session_file.write("model,method_type,time_elapsed_sec,complexity,rmse,nme,mae,mse,mape,smape,grubbs,shape_similarity\n")

    str_to_write = f"{method},{method_type},{elapsed_time_sec},{complexity},"

    rmse_score = round(rmse(predicted, real),2)
    nme_score = round(nme(predicted, real),2)
    mae_score = round(mae(predicted, real),2)
    mse_score = round(mse(predicted, real),2)
    mape_score = round(mape(predicted, real),2)
    smape_score = round(smape(predicted, real),2)

    # The current implementation of finding outliers, Grubbs, fails when all of the predicted values 
    # are the same since it causes a division by zero. Thus naive methods that predict the same value
    # are not automatically assigned a score of 0
    if method_type == 'Naive Methods' and method != 'random_walk':
        grubbs_test_score = 0
    else:
        grubbs_test_score = grubbs_score(predicted, real)
    shape_similarity_score = round(dtw(predicted, real),2)



    str_to_write += f"{rmse_score},{nme_score},{mae_score},{mse_score},{mape_score},{smape_score},{grubbs_test_score},{shape_similarity_score}\n"
    session_file.write(str_to_write)
    session_file.close()

# FORECASTING 
###########################################################################
def run_models(module_name, train, test, real, method_type):
    module = importlib.import_module(module_name)

    for name, function in module.__dict__.items():
        if callable(function) and name.startswith('predict_'):
            # Please note that mem usage wraps botth the function and the time measurement!
            start_time = time.time()
            predicted, complexity = function(train, test)
            end_time = time.time()
            # Memory usage is in mb while elapsed time is in seconds! 
            elapsed_time = end_time - start_time

            # Debugging
            # Expected object types: List / Pandas series
            # print(f"Predicted values type: {type(predicted)}")

            scoring(predicted, real, method_type, name, elapsed_time, complexity)
    
    string_to_return = eval_string()

    return string_to_return

# Creating data to test the functions if the user has not uploaded any
def import_test_data():
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    train = create_df_with_datetimes(train_df, 4)
    test = create_df_with_datetimes(test_df, 4)

    return train, test

# CONFIG FILE AND PRE-PROCESSING
###########################################################################
def get_user_file():
    pre_processing_check_config_object = ConfigParser()
    pre_processing_check_config_object.read("config.ini")

    #Get the SINGLESCOREINFO section
    config = pre_processing_check_config_object["USERFILE"]
    user_dataset_file = config['file_path']

    return user_dataset_file

def split_user_data():
    user_data_df = pd.read_csv(get_user_file())
    # 70-30 split with no fancy means
    split_index = int(0.7 * len(user_data_df))
    train = user_data_df[:split_index]
    test = user_data_df[split_index:]

    return train, test

def use_user_dataset():
    user_dataset_file = get_user_file()
    if user_dataset_file == 'empty':
        train, test = import_test_data()
    else:
        train, test = split_user_data()
    target_column_name = test.columns[1]
    real = test[target_column_name]

    return train, test, real

def allowed_file(filename):
    # Add the allowed file extensions here
    allowed_extensions = set(['csv', 'txt'])
    print(filename.rsplit('.',1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def pre_processing_passed():
    pre_processing_check_config_object = ConfigParser()
    pre_processing_check_config_object.read("config.ini")
    #Get the SINGLESCOREINFO section
    config = pre_processing_check_config_object["PREPROCESSING"]
    pre_processing_result = config['passed']

    if pre_processing_result == 'false':
        return False
    else:
        return True
    
def naive_run():
    check_config_object = ConfigParser()
    check_config_object.read("config.ini")

    #Get the SINGLESCOREINFO section
    config = check_config_object["MODELS"]
    has_naive_run = config['has_naive_run']

    if has_naive_run == 'false':
        print("Config naive run is false!")
        return False
    else:
        return True

def reset_config_file():
    # Update config file for confirm that naive methods have run 
    config_object = ConfigParser()
    config_object.read("config.ini")
    #Get the PREPROCESSING section
    config = config_object["MODELS"]
    config['has_naive_run'] = 'false'
    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    
    config = config_object["SINGLESCOREINFO"]
    config['accuracy'] = '5'
    config['outliers'] = '5'
    config['shape'] = '5'
    config['time'] = '5'
    config['naive'] = '5'
    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

    config = config_object["PREPROCESSING"]
    config['passed'] = 'false'
    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    
    config = config_object["USERFILE"]
    config['file_path'] = 'empty'
    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

# Wrapper here to run the function upon the application initialization
@app.before_first_request
def clear_session():
    try:
        if os.path.exists('session_file.csv'):
            session_file = open('session_file.csv', 'w')
            session_file.write("model,method_type,time_elapsed_sec,complexity,rmse,nme,mae,mse,mape,smape,grubbs,shape_similarity\n")
            session_file.close()
        else:
            session_file = open('session_file.csv', 'w')
            session_file.write("model,method_type,time_elapsed_sec,complexity,rmse,nme,mae,mse,mape,smape,grubbs,shape_similarity\n")
            session_file.close()
        
        if os.path.exists('Exports/output.txt'):
            output_file = open("Exports/output.txt", "w")
            output_file.write("This is an empty output file!")
            output_file.close()

        #Reseting the session file
        reset_config_file()

    except:
        print("Session reset failed!")

# ROUTING
###########################################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report')
def report():
    return render_template('report.html')

## INPUT FILE
@app.route('/upload-form', methods=['POST'])
def upload_file():

    # Check if a file was included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file extension', 'file extenstion': file.filename})

    shutil.copy(file.filename, "uploads")


    #Update config file
    config_object = ConfigParser()
    config_object.read("config.ini")
    #Get the SINGLESCOREINFO section
    config = config_object["USERFILE"]
    # request.form works with the elements' names 
    config['file_path'] = os.path.join('uploads', file.filename)
    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)

    pre_processing_result = pre_processing(file.filename)

    if pre_processing_result == True:
        return jsonify({'message': 'File uploaded successfully'})
    else: 
        print(pre_processing_result)
        return jsonify({'message': pre_processing_result})

# Reading and updating config files
@app.route('/slider-form', methods=['POST'])
def single_scoring_config():
    #Read config file
    scoring_config_object = ConfigParser()
    scoring_config_object.read("config.ini")

    #Get the SINGLESCOREINFO section
    scoring_config = scoring_config_object["SINGLESCOREINFO"]

    # Debugging 
    print(f"""Current vs New values: 
    accuracy: {scoring_config['accuracy']} | {request.form['slider1']} 
    outlier: {scoring_config['outliers']} | {request.form['slider2']} 
    shape: {scoring_config['shape']} | {request.form['slider3']} 
    time: {scoring_config['time']} | {request.form['slider4']} 
    complexity: {scoring_config['complexity']} | {request.form['slider5']} 
    naive: {scoring_config['naive']} | {request.form['slider6']}""")

    # request.form works with the elements' names 
    scoring_config['accuracy'] = request.form['slider1']
    scoring_config['outliers'] = request.form['slider2']
    scoring_config['shape'] = request.form['slider3']
    scoring_config['time'] = request.form['slider4']
    scoring_config['complexity'] = request.form['slider5']
    scoring_config['naive'] = request.form['slider6']

    #Write changes back to file
    with open('config.ini', 'w') as conf:
        scoring_config_object.write(conf)

    return jsonify({'message': 'Config file updated!'})

## FORECASTING
# ======================================================================================================================
# Traditional methods route
@app.route('/traditional_models', methods=['POST'])
def traditional_models():
    train, test, real = use_user_dataset()
    module_name = "traditional_models.traditional_models"
    if not pre_processing_passed():
        return jsonify({'result':'Error: Pre-processing has failed! Please re-upload your dataset'})
    elif not naive_run():
        return jsonify({'result':'Error: Naive methods must run first!'})
    else:
        result = run_models(module_name, train, test, real, 'Traditional Methods')
        return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})
        

# ML models route
@app.route('/ml_models', methods=['POST'])
def ml_models():
    train, test, real = use_user_dataset()
    module_name = "ml_models.ml_models"
    if not pre_processing_passed():
        return jsonify({'result':'Error: Pre-processing has failed! Please re-upload your dataset'})
    elif not naive_run():
        return jsonify({'result':'Error: Naive methods must run first!'})
    else:
        result = run_models(module_name, train, test, real, 'Machine Learning')
        return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})


# Naive methods route
@app.route('/naive_methods', methods=['POST'])
def naive_methods():
    train, test, real = use_user_dataset()
    module_name = "naive_methods.naive_methods"
    if pre_processing_passed():
        result = run_models(module_name, train, test, real, "Naive Methods")

        # Update config file for confirm that naive methods have run 
        config_object = ConfigParser()
        config_object.read("config.ini")
        #Get the PREPROCESSING section
        config = config_object["MODELS"]
        config['has_naive_run'] = 'true'
        #Write changes back to file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)

        return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})
        
    else:
        return jsonify({'result':'Error: Pre-processing has failed! Please re-upload your dataset'})
        


# EXPORTS
###########################################################################
@app.route('/export_results', methods=['POST'])
def export_results():
    export_file = open("Exports/output.txt", "w")
    #Some data first
    export_file.write(datetime.now().strftime("%m/%d/%Y, %H:%M"))
    export_file.write("\n")
    config_object = ConfigParser()
    config_object.read("config.ini")
    config = config_object["USERFILE"]
    export_file.write(f"Dataset: {config['file_path'].split(r'uploads/')[1]}")
    export_file.write("\n")
    export_file.write("================================================================")
    export_file.write("\n")
    
    #Data
    export_string = eval_string()
    export_file.write(export_string)
    export_file.write('\n')
    export_file.close()
    return jsonify({'result': 'File exported successfully -> Click "Download"'})

@app.route('/single_scores', methods=['POST'])
def export_single_scores():
    score()
    df = pd.read_csv("Exports/single_scores.csv")
    string_to_return = tabulate(df, headers='keys', tablefmt="grid")
    return jsonify({'result': 'Single scores file exported successfully -> Click "Download Single Score"',
                    'export': render_template_string('<pre>{{ data | safe }}</pre>', data=string_to_return)})


@app.route('/raw_results', methods=['POST'])
def export_raw_scores():
    shutil.copy("session_file.csv", "Exports/raw_results")
    shutil.copy("Exports/single_scores.csv", "Exports/raw_results")

    # Compressing results to a single file 
    # shutil.make_archive(zip_file_path, compress_type, directory_to_zip)
    shutil.make_archive("Exports/raw_results", 'zip', "Exports/raw_results")

    return jsonify({'result': 'Raw results files successfully created -> Click "Download Raw Result"'})


# DOWNLOAD FILE
@app.route('/Exports/<filename>')
def download_file(filename):
    return send_from_directory('Exports', filename, as_attachment=True)


# CLEAR RESULTS
###########################################################################
@app.route('/clear_results', methods=['POST'])
def clear_results():
    clear_session()
    return jsonify({'result': 'File clear successfully -> session_file.csv'})


if __name__ == '__main__':
    app.run(debug=True)
