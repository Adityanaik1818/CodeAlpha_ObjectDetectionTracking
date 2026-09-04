import cv2
import time
import threading
import queue
from detection.detector import ObjectTracker
from detection.annotator import FrameAnnotator
import config

# Global state dictionary to share live statistics with the Flask UI
live_stats = {
    "fps": 0.0,
    "current_detections": 0,
    "unique_objects": 0,
    "active": False
}

class FastVideoStream:
    """Dedicated background thread for zero-lag live webcam I/O."""
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
        
        self.q = queue.Queue(maxsize=1)
        self.stopped = False
        
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        while not self.stopped:
            ret, frame = self.stream.read()
            if not ret:
                self.stop()
                return
            if self.q.full():
                try: 
                    self.q.get_nowait()
                except queue.Empty: 
                    pass
            self.q.put(frame)
                
    def read(self):
        return self.q.get()
        
    def stop(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()
        self.stream.release()

def generate_frames(camera_index, conf_thresh: float):
    """Handles both live webcams and uploaded video files."""
    
    if isinstance(camera_index, int) or camera_index == '0':
        video_stream = FastVideoStream(int(camera_index))
        stream_is_live = True
    else:
        video_stream = cv2.VideoCapture(camera_index)
        stream_is_live = False
        if not video_stream.isOpened():
            live_stats["active"] = False
            return

    tracker = ObjectTracker(model_path=config.MODEL_NAME, conf_thresh=conf_thresh)
    live_stats["active"] = True
    seen_track_ids = set()
    prev_time = time.time()

    try:
        while True:
            if stream_is_live:
                frame = video_stream.read()
            else:
                success, frame = video_stream.read()
                if not success:
                    break # End of video file
            
            _, detections = tracker.process_frame(frame)
            
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            for det in detections:
                if det.track_id is not None:
                    seen_track_ids.add(det.track_id)
            
            live_stats["fps"] = round(fps, 1)
            live_stats["current_detections"] = len(detections)
            live_stats["unique_objects"] = len(seen_track_ids)

            FrameAnnotator.annotate(frame, detections, fps)

            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
            if not stream_is_live:
                time.sleep(0.03) # Prevent recorded videos from playing too fast
                
    finally:
        if stream_is_live:
            video_stream.stop()
        else:
            video_stream.release()
        live_stats["active"] = False