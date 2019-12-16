import responder
from werkzeug.utils import secure_filename
import controller
import subprocess
import json

UPLOAD_FOLDER = './uploads/'
api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})


@api.route('/')
def upload_image(req, resp):
    if req.method == "get":
        resp.text = "Hello World"


@api.route('/api/v1/upload')
async def uploaded_file(req, resp):
    if req.method == 'post':
        data = await req.media(format='files')
        if data['file'] and controller.allowed_file(data['file']['filename']):
            subprocess.run(['killall', 'led-image-viewe'])
            @api.background.task
            def process_file(file):
                filename = secure_filename(file['file']['filename'])
                image_path = UPLOAD_FOLDER + filename
                with open(image_path, 'wb') as f:
                    f.write(file['file']['content'])
                subprocess.run(['/usr/local/bin/led-image-viewer', image_path, '--led-slowdown-gpio=2'])
        process_file(data)
        resp.status_code = api.status_codes.HTTP_200
        resp.media = {'success': 'ok'}

    elif req.method != 'post':
        resp.status_code = api.status_codes.HTTP_405


@api.route('/api/v1/animation')
def changeAnimation(req, resp):
    if req.method == 'get':
        status = req.params.get("status", "")
        if status == 'true':
            subprocess.call('systemctl start ledTest.service')
            resp.status_code = api.status_codes.HTTP_200
        elif status == 'false':
            subprocess.call('systemctl stop ledTest.service')
            resp.status_code = api.status_codes.HTTP_200


@api.route('/api/v1/pictures')
def getPicturesList(req, resp):
    if req.method == 'get':
        picture_list = {"pictures": controller.get_pictures('./uploads/')}
        resp.headers = {"Content-Type": "application/json; charset=utf-8"}
        resp.content = json.dumps(picture_list, ensure_ascii=False)


if __name__ == '__main__':
    api.run(debug=True, address='0.0.0.0', port=5000)
