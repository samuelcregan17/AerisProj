import os
import tempfile
from PIL import Image
from CsvData import *
from flask import Flask, render_template, request

app = Flask(__name__)

# set up a temp dir that we can use to store input files and images
TEMP_DIR = tempfile.gettempdir()

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        # get the file that was uploaded through the request
        data_file = request.files.get('inputCsv')

        # if previous call returned nothing, we know we're coming from the "back" button of one of the
        # endpoint pages. No need to do anything to save the file because we already have it, so just
        # grab the file name and return the file uploaded page.
        if data_file is None:
            filepath = app.config['FULL_FILE_PATH']
            split = str.split(filepath, os.sep)
            filename = split[len(split) - 1]
            loaded_file_msg = "Loaded csv file name: " + filename
            return render_template('FileUploaded.html', message=loaded_file_msg)

        # set the file path to the temp dir
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], data_file.filename)

        # save the file to the temp dir and remember it in the app config to access later
        data_file.save(filepath)
        app.config['FULL_FILE_PATH'] = filepath

        loaded_file_msg = "Loaded csv file name: " + data_file.filename

        return render_template('FileUploaded.html', message=loaded_file_msg)
    return render_template('MainWindowView.html')


@app.route('/get-mean')
def get_mean():
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_mean()
    return render_template('StatisticalComputation.html',
                           operation="Mean",
                           result=result,
                           confettiPath=os.path.join(os.getcwd(), "js", "confetti.js"))


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
    data = CsvData(app.config['FULL_FILE_PATH'])
    image = data.get_image()
    img_filepath = os.path.join(app.config["UPLOAD_FOLDER"], "pngRepresentation.png")
    image.save(img_filepath)
    return render_template('PngRepresentation.html', img_filepath=img_filepath)
