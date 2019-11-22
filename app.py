import os
from flask import Flask, request, flash, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from controller import allowed_file
import subprocess

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'hogehoge'
CORS(app)


@app.route('/', methods=['GET'])
def upload_image():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
    print(request.files)
    if 'file' not in request.files:
        flash('ファイルがありません')
    file = request.files['file']
    if file.filename == '':
        flash('ファイルがありません')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = app.config['UPLOAD_FOLDER'] + '/' + filename
        subprocess.run(['killall', 'led-image-viewe'])
        subprocess.run(['/usr/local/bin/led-image-viewer', image_path, '--led-slowdown-gpio=2'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
