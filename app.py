from pathlib import Path

import responder
import controller
import subprocess
import json

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
        controller.show_image(data)
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


@api.route('/api/v1/face')
def emotionPattern(req, resp):
    if req.method == 'get':
        emotion = req.params.get("emotion", "")
        if emotion == "anger":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "contempt":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "disgust":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "fear":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "happiness":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "neutral":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "sadness":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200
        elif emotion == "surprise":
            controller.show_image(None)
            resp.status_code = api.status_codes.HTTP_200


if __name__ == '__main__':
    api.run(debug=True, address='0.0.0.0', port=5000)
