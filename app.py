from flask import Flask, render_template, request
from fileinput import filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        return render_template('FileUploaded.html')
    return render_template('MainWindowView.html')