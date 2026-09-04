from dataclasses import dataclass
from typing import List, Tuple, Any
from ultralytics import YOLO

@dataclass
class Detection:
    """Clean representation of a single detected and tracked object."""
    class_id: int
    class_name: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int
    track_id: int | None

class ObjectTracker:
    """Core Computer Vision abstraction handling YOLOv8 inference and tracking."""
    
    def __init__(self, model_path: str = "yolov8n.pt", conf_thresh: float = 0.40):
        # Load the model strictly ONCE during initialization
        self.model = YOLO(model_path)
        self.conf_thresh = conf_thresh
        self.class_names = self.model.names

    def process_frame(self, frame: Any) -> Tuple[Any, List[Detection]]:
        """
        Runs YOLO tracking on a single OpenCV frame.
        Returns the raw results object and a list of structured Detections.
        """
        # persist=True enables multi-object tracking (ByteTrack by default in Ultralytics)
        results = self.model.track(frame, persist=True, conf=self.conf_thresh, verbose=False)
        
        result = results[0]
        detections = []
        
        if result.boxes is not None and result.boxes.id is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            track_ids = result.boxes.id.int().cpu().tolist()
            class_ids = result.boxes.cls.int().cpu().tolist()
            confs = result.boxes.conf.cpu().tolist()

            for box, track_id, class_id, conf in zip(boxes, track_ids, class_ids, confs):
                det = Detection(
                    class_id=class_id,
                    class_name=self.class_names[class_id],
                    confidence=round(conf, 2),
                    x1=int(box[0]),
                    y1=int(box[1]),
                    x2=int(box[2]),
                    y2=int(box[3]),
                    track_id=track_id
                )
                detections.append(det)
                
        return result, detections