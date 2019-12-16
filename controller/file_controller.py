from pathlib import Path
from itertools import chain
import models


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
