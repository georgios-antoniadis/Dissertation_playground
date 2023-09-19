from flask import Flask, render_template, request, jsonify
import os
from tkinter import *

# import filedialog module
from tkinter import filedialog

# My custom evaluation protocol
from evaluation_protocol.grubbs import grubbs_score
from evaluation_protocol.mape import mape
from evaluation_protocol.smape import smape
from evaluation_protocol.shape_similarity import dtw

# Models


app = Flask(__name__)

result = ''
export = 'This is the export file'

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

@app.route('/function2', methods=['POST'])
def function2():
    result = "Function 2"
    return jsonify({'result': result})

@app.route('/function3', methods=['POST'])
def function3():
    result = "Function 3"
    return jsonify({'result': result})

@app.route('/function4', methods=['POST'])
def function4():
    result = "Function 4"
    return jsonify({'result': result})

@app.route('/exportResults', methods=['POST'])
def exportResults():
    export_file = open("output.txt", "w")
    export_file.write(export)
    export_file.write('\n')
    return jsonify({'result': 'File exported successfully -> output.txt'})


if __name__ == '__main__':
    app.run(debug=True)
