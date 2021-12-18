from os import path
from flask import Flask, Response, request, send_file
from flask import request
from flask_cors import CORS
from facerec_rtree import KNNRtree, encode
import base64, json, os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SAVE_FOLDER = 'data/saved'
fileCount = 1

app = Flask(__name__)
cors = CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_image():
    global fileCount
    data = json.loads(request.data)
    if 'file' not in data:
        msg = 'File not found'
        return Response(json.dumps(msg))
    if data['file'] == None:
        return 'Invalid file'
    numResults = data['results']
    print(numResults)
    imageParts = data['file'].split(';base64,')
    file = base64.b64decode(imageParts[1])
    filename = '{}/uploaded-file-{}.jpeg'.format(SAVE_FOLDER, str(fileCount))
    with open(filename, 'wb+') as f:
        f.write(file)
    fileCount += 1
    # Process image
    result = list(KNNRtree(int(numResults), encode(filename), 2000))
    print(result)
    msg = []
    for r in result:
        path = os.path.join(r['path'], r['name'])
        name = r['name']
        nameParts = name.split('_')
        name = nameParts[0] + ' ' + nameParts[1]
        image = base64.b64encode(open(path, 'rb').read())
        msg.append({'name': name, 'image': image.decode('ascii')})
    # print(msg)
    return Response(json.dumps(msg), 200)


# def processImage(img):
#     encoding = images.getEncoding(img)
#     print(encoding)
