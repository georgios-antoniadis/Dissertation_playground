from flask import Flask, render_template, request, jsonify, render_template_string
import os
from tkinter import *
import pandas as pd

# import filedialog module
from tkinter import filedialog

# My custom evaluation protocol
from evaluation_protocol.grubbs import grubbs_score
from evaluation_protocol.mape import mape
from evaluation_protocol.smape import smape
from evaluation_protocol.shape_similarity import dtw
from evaluation_protocol.evaluation_protocol_string import eval_string

# Models
from naive_methods.last_value import predict_last_value
from naive_methods.m4_naive import m4_naive
from naive_methods.only_mean import mean_naive
from naive_methods.random_walk import random_walk

from ml_models.lightgbm import lightgbm
from ml_models.prophet_model import prophet_model

from traditional_models.arima import arima_model
from traditional_models.theta_model import theta_model_forecast

# Dataset
from handle_dataset.transform import create_df_with_datetimes

app = Flask(__name__)

result = ''
export = 'This is the export file'

train_file = 'Dataset/Yearly-train.csv'
test_file = 'Dataset/Yearly-test.csv'

# For grubbs score 
alpha = 0.05

# Printing the evaluation protocol string
def create_eval_string(predicted_dictionary, scores_dict, real, method_type):
    created_string = f'{method_type}\n'
    created_string += '- ' * len(method_type) + '\n'
    for key in predicted_dictionary:
        predicted = predicted_dictionary[key]
        grubbs_test_score = grubbs_score(predicted, real, alpha)
        smape_score = smape(real, predicted)
        shape_similarity_score = dtw(predicted, real)
        mape_score = mape(real, predicted)

        # MAPE | sMAPE | Grubbs | tShape similarity
        scores_dict[key].append(round(mape_score,2))
        scores_dict[key].append(round(smape_score,2))
        scores_dict[key].append(round(grubbs_test_score))
        scores_dict[key].append(round(shape_similarity_score))
    
    created_string += eval_string(score_dict=scores_dict)

    return created_string

# Creating data to test the functions
def import_test_data():

    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    train = create_df_with_datetimes(train_df, 0)
    test = create_df_with_datetimes(test_df, 0)

    return train, test





@app.route('/')
def index():
    return render_template('index.html')

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

    return jsonify({'message': 'File uploaded successfully'})

def allowed_file(filename):
    # Add the allowed file extensions here
    allowed_extensions = set(['csv', 'txt'])
    print(filename.rsplit('.',1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

## BUTTONS
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

    scores_dict = {
        'arima': [],
        'theta': []
    }

    train, test = import_test_data()

    target_column_name = test.columns[1]
    real = test[target_column_name]

    # Forecast periods!! 
    arima_forecasts = arima_model(series=train['target'].astype(float), forecast_periods=6)
    theta_forecasts = theta_model_forecast(series=train['target'], h=len(test))

    predicted_dictionary = {"arima": arima_forecasts,
                        "theta": theta_forecasts}


    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Traditional Methods')

    # Debugging
    # result = eval_string(scores_dict)
    # print(result)
    # return jsonify({'result': result})
    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})


# ML models route
@app.route('/ml_models', methods=['POST'])
def ml_models():

    scores_dict = {
        'prophet': []
    }

    train, test = import_test_data()

    target_column_name = test.columns[1]
    real = test[target_column_name]

    prophet_forecasts = prophet_model(train=train, test=test)


    predicted_dictionary = {"prophet": prophet_forecasts
                            }

    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Machine Learning')

    # Debugging
    # result = eval_string(scores_dict)
    # print(result)
    # return jsonify({'result': result})
    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})



@app.route('/naive_methods', methods=['POST'])
def naive_methods():

    train, test = import_test_data()

    target_column_name = test.columns[1]
    real = test[target_column_name]

    last_value_forecasts = predict_last_value(train['target'].tolist(), len(test))
    mean_naive_forecasts = mean_naive(train['target'].tolist(), len(test))
    random_walk_forecasts = random_walk(train['target'].tolist(), len(test))
    
    predicted_dictionary = {
        "last_value": last_value_forecasts,
        "mean_naive": mean_naive_forecasts,
        "random_walk": random_walk_forecasts
                            }

    scores_dict = {
        'last_value': [],
        'mean_naive': [],
        'random_walk': []
    }


    result = create_eval_string(predicted_dictionary, scores_dict, real, 'Naive Methods')
    # Debugging
    # print(result)
    # return jsonify({'result': result})
    return jsonify({'result':render_template_string('<pre>{{ data | safe }}</pre>', data=result)})



@app.route('/exportResults', methods=['POST'])
def exportResults():
    export_file = open("output.txt", "w")
    export_file.write(export)
    export_file.write('\n')
    return jsonify({'result': 'File exported successfully -> output.txt'})


if __name__ == '__main__':
    app.run(debug=True)