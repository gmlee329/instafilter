from instafilter import Instafilter
import cv2
from PIL import Image
import numpy as np
import os
import uuid
import shutil
import io
from werkzeug.utils import secure_filename

# import for server
from flask import Flask, render_template, request, Response, send_file, jsonify
from queue import Queue, Empty
import threading
import time

# flask server
app = Flask(__name__)

# limit input file size under 2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

# model loading
model = Instafilter('Crema')

# request queue setting
requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

# static variable
models = ['1977', 'Aden', 'Amaro', 'Ashby', 'Brannan', 'Brooklyn', 'Charmes', 'Clarendon', 'Crema', 
        'Dogpatch', 'Earlybird', 'Gingham', 'Ginza', 'Hefe', 'Helena', 'Hudson', 'Inkwell', 'Juno', 
        'Kelvin', 'Lark', 'Lo-Fi', 'Ludwig', 'Mayfair', 'Melvin', 'Moon', 'Nashville', 'Perpetua', 
        'Reyes', 'Rise', 'Sierra', 'Skyline', 'Slumber', 'Stinson', 'Sutro', 'Toaster', 'Valencia', 
        'Vesper', 'Walden', 'Willow', 'X-ProII']
INPUT_DIR = './input'
POSIBLE_FORMAT = ['image/jpeg', 'image/jpg', 'image/png']

# request handling
def handle_requests_by_batch():
    try:
        while True:
            requests_batch = []
            while not (len(requests_batch) >= BATCH_SIZE):
                try:
                    requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
                except Empty:
                    continue
                
            batch_outputs = []

            for request in requests_batch:
                batch_outputs.append(run(request["input"][0], request["input"][1]))

            for request, output in zip(requests_batch, batch_outputs):
                request["output"] = output

    except Exception as e:
        while not requests_queue.empty():
            requests_queue.get()
        print(e)


# request processing
threading.Thread(target=handle_requests_by_batch).start()

def byte_to_image(image_byte):
    open_image = Image.open(io.BytesIO(image_byte))
    image = rgba_to_rgb(open_image)
    return image
    
def rgba_to_rgb(open_image):
    if open_image.mode == 'RGBA':
        image = Image.new('RGB', open_image.size, (255, 255, 255))
        image.paste(open_image, mask=open_image.split()[3])
    else:
        image = open_image.convert('RGB')
    return image

def remove_file(paths):
    for path in paths:
        shutil.rmtree(path)

def image_to_byte(image):
    byte_io = io.BytesIO()
    image.save(byte_io, "PNG")
    byte_io.seek(0)
    return byte_io

# run model
def run(mode, image_file):
    try:
        # read image_file
        f_id = str(uuid.uuid4())
        f_name = secure_filename(image_file.filename)
        image_byte = image_file.read()
        image = byte_to_image(image_byte)

        # make input&result file folder
        paths = [os.path.join(INPUT_DIR, f_id)]
        os.makedirs(paths[0], exist_ok=True)

        # save image to input folder
        in_filename = os.path.join(paths[0], f_name)
        image.save(in_filename, quality=100, subsampling=0)

        # run model
        model = Instafilter(mode)
        new_image = model(in_filename)

        # convert nparray to image
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        ouput_image = Image.fromarray(new_image)

        # convert result image to byte format
        byte_image = image_to_byte(ouput_image)

        return byte_image

    except Exception as e:
        print(e)
        return 500

    finally:
        # remove input folder
        if paths:
            remove_file(paths)
            paths.clear()

# routing
@app.route("/filter", methods=['POST'])
def apply_filter():
    try:
        # only get one request at a time
        if requests_queue.qsize() > BATCH_SIZE:
            return jsonify({'message' : 'TooManyReqeusts'}), 429
    
        # check image format
        try:
            image_file = request.files['image']
        except Exception:
            return jsonify({'message' : 'Image size is larger than 2MB'}), 400
    
        if image_file.content_type not in POSIBLE_FORMAT:
            return jsonify({'message' : 'Only support jpg, jpeg, png'}), 400
        
        try:
            available = False
            mode = str(request.form['mode'])
            for modes in models:
                if mode.lower() == modes.lower():
                    mode = modes
                    available = True
                    break
            if not available:
                return jsonify({'message' : 'That mode not supported'}), 400
        except Exception:
            return jsonify({'message' : 'Error! An unknown error occurred on the server'}), 500

        # put data to request_queue
        req = {'input' : [mode, image_file]}
        requests_queue.put(req)

        # wait output
        while 'output' not in req:
            time.sleep(CHECK_INTERVAL)
        
        # send output
        byte_image = req['output']

        if byte_image == 500:
            return jsonify({'message': 'Error! An unknown error occurred on the server'}), 500
        
        result = send_file(byte_image, mimetype="image/png")
        
        return result
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error! Unable to process request'}), 400

@app.route('/healthz')
def health():
    return "ok", 200

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)