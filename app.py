import os
import tempfile
from CsvData import *
from flask import Flask, render_template, request

app = Flask(__name__)

# set up a temp dir that we can use to store input files
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        # get the file that was uploaded through the request
        data_file = request.files.get('inputCsv')

        # set the file path to the temp dir
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], data_file.filename)

        # save the file to the temp dir and remember it in the app config to access later
        data_file.save(filepath)
        app.config['FULL_FILE_PATH'] = filepath;

        loaded_file_msg = "Loaded csv file name: " + data_file.filename

        return render_template('FileUploaded.html', message=loaded_file_msg)
    return render_template('MainWindowView.html')


@app.route('/get-mean')
def get_mean():
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_mean()
    return render_template('StatisticalComputation.html',
                           operation="Mean",
                           result=result)


@app.route('/get-std-deviation')
def get_std_deviation():
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_std_deviation()
    return render_template('StatisticalComputation.html',
                           operation="Standard Deviation",
                           result=result)


@app.route('/get-sum')
def get_sum():
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_sum()
    return render_template('StatisticalComputation.html',
                           operation="Sum",
                           result=result)


@app.route('/get-image')
def get_image():
    return
