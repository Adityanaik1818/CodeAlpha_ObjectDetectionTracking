import os
from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import cv2
import numpy as np
import config
from utils.video import generate_frames, live_stats
from detection.detector import ObjectTracker
from detection.annotator import FrameAnnotator

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

static_tracker = ObjectTracker(model_path=config.MODEL_NAME, conf_thresh=config.DEFAULT_CONFIDENCE)
current_video_source = config.DEFAULT_CAMERA_INDEX

@app.route('/')
def index():
    return render_template('index.html', title=config.DASHBOARD_TITLE, current_source=str(current_video_source))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(current_video_source, config.DEFAULT_CONFIDENCE),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/stats')
def stats():
    return jsonify(live_stats)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    _, detections = static_tracker.process_frame(img)
    FrameAnnotator.annotate(img, detections, fps=0.0)
    
    ret, buffer = cv2.imencode('.jpg', img)
    return Response(buffer.tobytes(), mimetype='image/jpeg')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global current_video_source
    if 'file' not in request.files:
        return redirect(url_for('index'))
        
    file = request.files['file']
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)
    
    current_video_source = filepath
    return redirect(url_for('index'))

@app.route('/reset_webcam', methods=['POST'])
def reset_webcam():
    global current_video_source
    current_video_source = config.DEFAULT_CAMERA_INDEX
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)