import os
import tempfile
from flask import Flask, render_template, request

app = Flask(__name__)

# set up a temp dir that we can use to store input files
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        # get the file that was uploaded through the request
        data_file = request.files.get('inputCsv')

        # save the file to the temp dir to access later
        data_file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                    data_file.filename))

        loaded_file_msg = "Loaded csv file name: " + data_file.filename

        return render_template('FileUploaded.html', message=loaded_file_msg)
    return render_template('MainWindowView.html')


@app.route('/get-mean')
def get_mean():
    return


@app.route('/get-std-deviation')
def get_std_deviation():
    return


@app.route('/get-sum')
def get_sum():
    return


@app.route('/get-image')
def get_image():
    return
