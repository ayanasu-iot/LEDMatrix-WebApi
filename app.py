import os
from flask import Flask, request, send_from_directory, flash, render_template
from werkzeug.utils import secure_filename, redirect
from controller import *
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = app.config['UPLOAD_FOLDER'] + '/' + filename
            #controller.showImage(image_path)
            subprocess.run(['/usr/local/bin/led-image-viewer', image_path, '--led-no-hardware-pulse'])
            return redirect(request.url)
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
