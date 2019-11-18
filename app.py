from flask import Flask, request
# from controller import controller

app = Flask(__name__)


@app.route('/', methods=['POST'])
def show():
    if request.headers['Content-Type'] == 'application/json':
        json = request.get_json()
        print(json['image'])
        # controller.showImage(json['image'])
    return request.get_data()


if __name__ == '__main__':
    app.run(debug=True)
