from flask import Flask, render_template, request, jsonify, render_template_string
import os
from tkinter import *
import pandas as pd
import importlib
import time
from memory_profiler import profile, memory_usage
# import filedialog module
from tkinter import filedialog

# My custom evaluation protocol
from evaluation_protocol.grubbs import grubbs_score
from evaluation_protocol.mape import mape
from evaluation_protocol.smape import smape
from evaluation_protocol.shape_similarity import dtw
from evaluation_protocol.result_string import eval_string
# from evaluation_protocol.evaluation_protocol import eval_protocol

# Dataset
from handle_dataset.transform import create_df_with_datetimes

app = Flask(__name__)

result = ''
export = 'This is the export file'

train_file = 'Dataset/Yearly-train.csv'
test_file = 'Dataset/Yearly-test.csv'

user_dataset_file = ''

# For grubbs score 
alpha = 0.05

# Printing the evaluation protocol string
def create_eval_string(predicted_dictionary, scores_dict, real, method_type):
    created_string = f'{method_type}\n'
    created_string += '- ' * len(method_type) + '\n'
    for key in predicted_dictionary:
        predicted = predicted_dictionary[key]
        # Grubbs score makes no sense for methods that predict the last value or the mean
        if method_type == 'Naive Methods' and key != 'random_walk':
            grubbs_test_score = 0
        else:
            grubbs_test_score = grubbs_score(predicted, real, alpha)
        smape_score = smape(real, predicted)
        shape_similarity_score = dtw(predicted, real)
        mape_score = mape(real, predicted)

        # MAPE | sMAPE | Grubbs | tShape similarity
        scores_dict[key].append(round(mape_score,2))
        scores_dict[key].append(round(smape_score,2))
        scores_dict[key].append(round(grubbs_test_score))
        scores_dict[key].append(round(shape_similarity_score))
    
    created_string += eval_string(scores_dict=scores_dict)

    return created_string

# Creating data to test the functions
def import_test_data():

    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    train = create_df_with_datetimes(train_df, 4)
    test = create_df_with_datetimes(test_df, 4)

    return train, test


def confirm_dataset_structure(uploaded_file_path):
    file_df = pd.read_csv(uploaded_file_path)
    flag = False
    if file_df.columns == ['timestamp','target']:
        flag = True
    else:
        flag = False
    
    return flag

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

def split_user_data():

    user_data_df = pd.read_csv(user_dataset_file)

    # 70-30 split with no fancy means
    split_index = int(0.7 * len(user_data_df))

    train = user_data_df[:split_index]
    test = user_data_df[split_index:]

    return train, test

def run_models(module_name, train, test):
    # module_name = "traditional_models.traditional_models"
    module = importlib.import_module(module_name)

    predicted_dictionary = {}
    scores_dict = {}

    for name, function in module.__dict__.items():
        if callable(function) and name.startswith('predict_'):
            scores_dict[name] = []
            # Please note that mem usage wraps botth the function and the time measurement!
            mem_usage_before = memory_usage()[0]
            start_time = time.time()
            predicted_dictionary[name] = function(train, test)
            end_time = time.time()
            mem_usage_after = memory_usage()[0]
            # Memory usage is in mb while elapsed time is in seconds! 
            mem_usage = mem_usage_after - mem_usage_before
            elapsed_time = end_time - start_time
            scores_dict[name].append(round(elapsed_time,4))
            scores_dict[name].append(mem_usage)

    return predicted_dictionary, scores_dict

def use_user_dataset():
    if user_dataset_file == '':
        train, test = import_test_data()
    else:
        train, test = split_user_data()

    target_column_name = test.columns[1]
    real = test[target_column_name]

    return train, test, target_column_name, real

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

    # Save the uploaded file to a specific location
    file.save(os.path.join('uploads', file.filename))
    global user_dataset_file 
    user_dataset_file = os.path.join('uploads', file.filename)
    return jsonify({'message': 'File uploaded successfully'})

def allowed_file(filename):
    # Add the allowed file extensions here
    allowed_extensions = set(['csv', 'txt'])
    print(filename.rsplit('.',1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

## BUTTON CALLS
# ======================================================================================================================
@app.route('/function1', methods=['POST'])
def function1():
    for file in os.listdir('uploads'):
        data_file = open(os.path.join('uploads',file), 'r')
        file_lines = data_file.readlines()
        from_file = len(file_lines)
    result = f'Function 1: Lines in file = {from_file}'
    return jsonify({'result': result})
    # return render_template('index.html', result=result)


# Traditional methods route
@app.route('/traditional_models', methods=['POST'])
def traditional_models():
    train, test, target_column_name, real = use_user_dataset()
    module_name = "traditional_models.traditional_models"
    predicted_dictionary, scores_dict = run_models(module_name, train, test)
    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Traditional Methods')

    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})


# ML models route
@app.route('/ml_models', methods=['POST'])
def ml_models():
    train, test, target_column_name, real = use_user_dataset()
    module_name = "ml_models.ml_models"
    predicted_dictionary, scores_dict = run_models(module_name, train, test)
    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Machine Learning')

    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})



@app.route('/naive_methods', methods=['POST'])
def naive_methods():
    train, test, target_column_name, real = use_user_dataset()
    module_name = "naive_methods.naive_methods"
    predicted_dictionary, scores_dict = run_models(module_name, train, test)
    # final_dict = eval_protocol(
    #     predicted_dictionary=predicted_dictionary, 
    #     real=real, 
    #     method_type='Naive Methods',
    #     scores_dict = scores_dict) 
    # result = eval_string()
    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Naive Methods')
    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})


# EXPORT RESULTS
@app.route('/exportResults', methods=['POST'])
def exportResults():
    export_file = open("output.txt", "w")
    export_file.write(export)
    export_file.write('\n')
    return jsonify({'result': 'File exported successfully -> output.txt'})


if __name__ == '__main__':
    app.run(debug=True)
