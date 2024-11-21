from flask import Flask, jsonify, Response, send_from_directory , request , send_file , redirect , url_for
import subprocess
import os
from threading import Lock
import zmq
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Configuration
presentation_folder = "presentation"

# Configure Flask using environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# ZMQ context and sockets
context = zmq.Context()
video_socket = context.socket(zmq.SUB)
video_socket.connect("tcp://localhost:5555")
video_socket.setsockopt_string(zmq.SUBSCRIBE, "")
slide_socket = context.socket(zmq.SUB)
slide_socket.connect("tcp://localhost:5556")
slide_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Threading control
process1 = None
process2 = None
thread_lock = Lock()

@app.route('/')
def home():
    return "Hello, Flask!"

# Serve frontend index.html
@app.route('/frontend')
def serve_index():
    return send_file('D:/Project/frontend/index.html')

# Serve other frontend assets (JavaScript, CSS, images)
@app.route('/frontend/<path:path>')
def serve_frontend(path):
    return send_from_directory('D:/Project/frontend', path)
    

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = 'D:/Project/backend/PPT'
ALLOWED_EXTENSIONS = {'pptx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pptxFile' not in request.files:
        return jsonify({'status': 'No file part'}), 400
    file = request.files['pptxFile']
    if file.filename == '':
        return jsonify({'status': 'No selected file'}), 400
    if file and file.filename.endswith('.pptx'):
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Now execute test.py script
        try:
            # Run the test.py script
            result = subprocess.run(['python', 'test.py'], capture_output=True, text=True)
            # If needed, process the result here
            print(result.stdout)  # You can log or process the output of test.py

            return jsonify({'status': 'File uploaded and test.py executed!'}), 200
        except Exception as e:
            print(e)
            return jsonify({'status': 'File upload successful, but error running test.py'}), 500

    return jsonify({'status': 'Invalid file type'}), 400
        

@app.route('/api/start1', methods=['GET'])
def start_presentation1():
    global process1
    with thread_lock:
        if process1 is None or process1.poll() is not None:
            process1 = subprocess.Popen(['python', 'test.py'])
            return jsonify({"status": "Presentation 1 started"}), 200
        else:
            return jsonify({"status": "Presentation 1 already running"}), 200


@app.route('/api/start2', methods=['GET'])
def start_presentation2():
    global process2
    with thread_lock:
        if process2 is None or process2.poll() is not None:
            process2 = subprocess.Popen(['python', 'slider.py'])
            return jsonify({"status": "Presentation 2 started"}), 200
        else:
            return jsonify({"status": "Presentation 2 already running"}), 200

@app.route('/api/stop1', methods=['GET'])
def stop_presentation1():
    global process1
    with thread_lock:
        if process1 is not None and process1.poll() is None:
            process1.terminate()
            process1.wait()
            return jsonify({"status": "Presentation 1 stopped"}), 200
        else:
            return jsonify({"status": "No presentation 1 running"}), 200

@app.route('/api/stop2', methods=['GET'])
def stop_presentation2():
    global process2
    with thread_lock:
        if process2 is not None and process2.poll() is None:
            process2.terminate()
            process2.wait()
            return jsonify({"status": "Presentation 2 stopped"}), 200
        else:
            return jsonify({"status": "No presentation 2 running"}), 200

@app.route('/api/slides', methods=['GET'])
def get_slides():
    slides = sorted(os.listdir(presentation_folder), key=len)
    return jsonify({"slides": slides})

@app.route('/slides/<filename>')
def get_slide(filename):
    return send_from_directory(presentation_folder, filename)

def generate_video_frames():
    while True:
        frame = video_socket.recv()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_slide_frames():
    while True:
        frame = slide_socket.recv()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/slide_feed')
def slide_feed():
    return Response(generate_slide_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
