import cv2
from typing import List
from detection.detector import Detection

class FrameAnnotator:
    """Handles all OpenCV drawing operations independently of the detection logic."""
    
    @staticmethod
    def annotate(frame, detections: List[Detection], fps: float) -> None:
        """Draws bounding boxes, tracking IDs, and FPS on the frame in-place."""
        # Draw Detections
        for det in detections:
            # Color based on track_id for visual separation
            color = ((det.track_id * 50) % 255, (det.track_id * 80) % 255, (det.track_id * 110) % 255)
            
            # Bounding box
            cv2.rectangle(frame, (det.x1, det.y1), (det.x2, det.y2), color, 2)
            
            # Label background
            label = f"{det.class_name} | ID:{det.track_id} | {det.confidence:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (det.x1, det.y1 - 20), (det.x1 + w, det.y1), color, -1)
            
            # Label text
            cv2.putText(frame, label, (det.x1, det.y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Draw FPS counter
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)