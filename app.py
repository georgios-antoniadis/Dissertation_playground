from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

result = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/function1', methods=['POST'])
def function1():
    result = "Function 1"
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


if __name__ == '__main__':
    app.run(debug=True)
