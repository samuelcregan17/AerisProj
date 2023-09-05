import os
import tempfile
from PIL import Image
from CsvData import *
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# set up the paths to the static folder which will hold the uploaded files and our png images
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def start_page():
    """ Initial entry point of the application. Will return either the home page or the analysis page,
    depending whether we are dealing with a GET or POST method."""
    if request.method == 'POST':
        # get the file that was uploaded through the request
        data_file = request.files.get('inputCsv')

        # if previous call returned nothing, we know we're coming from the "back" button of one of the
        # endpoint pages because there was no request. No need to do anything to save the file because
        # we already have it, so just grab the file name and return the analysis page.
        if data_file is None:
            filepath = app.config['FULL_FILE_PATH']
            split = str.split(filepath, os.sep)
            filename = split[len(split) - 1]
            loaded_file_msg = "Loaded csv file name: " + filename
            return render_template('AnalysisPage.html', message=loaded_file_msg)

        if data_file.filename == '':
            return redirect(request.url)

        # set the file path to the temp dir
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], data_file.filename)

        # save the file to the temp dir and remember it in the app config to access later
        data_file.save(filepath)

        # check if the file passes our validation (currently only validation is checking for the
        # "concentration" header
        if not validate_file(filepath):
            return redirect(request.url)

        app.config['FULL_FILE_PATH'] = filepath

        loaded_file_msg = "Loaded csv file name: " + data_file.filename

        return render_template('AnalysisPage.html', message=loaded_file_msg)
    return render_template('HomePage.html')


def validate_file(csv_path):
    """Validates a csv file to determine if it contains a header column containing the string "concentration"
    The input param is a string to the exact path of the csv file to validate."""
    file = open(csv_path)
    csvreader = csv.reader(file)

    header = csvreader.__next__()
    try:
        index = header.index("concentration")
        return True
    except ValueError:
        return False


@app.route('/get-mean')
def get_mean():
    """Get the mean of the concentration column and display in a new html page."""
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_mean()
    return render_template('StatisticalComputationPage.html',
                           operation="Mean",
                           result=result)


@app.route('/get-std-deviation')
def get_std_deviation():
    """Get the standard deviation of the concentration column and display in a new html page."""
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_std_deviation()
    return render_template('StatisticalComputationPage.html',
                           operation="Standard Deviation",
                           result=result)


@app.route('/get-sum')
def get_sum():
    """Get the sum of the concentration column and display in a new html page."""
    data = CsvData(app.config['FULL_FILE_PATH'])
    result = data.get_sum()
    return render_template('StatisticalComputationPage.html',
                           operation="Sum",
                           result=result)


@app.route('/get-image')
def get_image():
    """Get a PNG image representation of the concentration column and display in a new html page."""
    data = CsvData(app.config['FULL_FILE_PATH'])
    image = data.get_image()
    img_filepath = os.path.join(app.config["UPLOAD_FOLDER"], "pngRepresentation.png")
    image.save(img_filepath)
    return render_template('PngRepresentationPage.html',
                           img_filepath=img_filepath,
                           minimum=data.get_min(),
                           maximum=data.get_max())


@app.route("/show-help")
def show_help():
    """Show the README.md documentation in a new page."""
    return render_template('HelpPage.html',
                           readme_path=os.path.join(os.getcwd(), "README.md"))
