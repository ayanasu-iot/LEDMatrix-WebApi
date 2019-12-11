import responder
from werkzeug.utils import secure_filename
from controller import allowed_file
import subprocess

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


@api.route('/upload')
async def uploaded_file(req, resp):
    if req.method == 'post':
        data = await req.media(format='files')
        if data['file'] and allowed_file(data['file']['filename']):
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

if __name__ == '__main__':
    api.run(debug=True, address='0.0.0.0', port=5000)
