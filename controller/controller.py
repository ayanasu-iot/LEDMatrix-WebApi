from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


def _initMatrix():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'
    return RGBMatrix(options=options)


def showImage(image_file):
    matrix = _initMatrix()
    image = Image.open(image_file)
    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(image.convert('RGB'))
