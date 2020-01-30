import subprocess
import time
from pathlib import Path
from itertools import chain
from werkzeug.utils import secure_filename

import models
from app import api


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in models.ALLOWED_EXTENSIONS


def get_pictures(filepath):
    p = Path(filepath)
    gen = (p.glob("./*.{}".format(i)) for i in models.ALLOWED_EXTENSIONS)
    png_files = gen.__next__()
    jpg_files = gen.__next__()
    gif_files = gen.__next__()
    result = chain(png_files, jpg_files, gif_files)
    return [str(i) for i in result]


@api.background.task
def show_image(file):
    filename = secure_filename(file['file']['filename'])
    image_path = models.UPLOAD_FOLDER + filename
    with open(image_path, 'wb') as f:
        f.write(file['file']['content'])
    time.sleep(2)
    subprocess.run(['/usr/local/bin/led-image-viewer', image_path, '--led-slowdown-gpio=2'])


@api.background.task
def display_emotion(filename):
    subprocess.run(['killall', 'led-image-viewe'])
    image_path = models.STATIC_FOLDER + filename
    subprocess.run(['/usr/local/bin/led-image-viewer', image_path, '--led-slowdown-gpio=2'])
