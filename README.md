# 👁️ VisionTrack AI
### Real-Time Object Detection & Tracking System • CodeAlpha Task 4

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg" alt="YOLOv8">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 🚀 Overview

**VisionTrack AI** is a production-grade, multi-input Computer Vision dashboard engineered for real-time object detection and persistent tracking. Built as part of CodeAlpha Task 4, this system seamlessly bridges high-performance deep learning inference with a clean, ultra-responsive web interface, delivering zero-lag video processing and dynamic live statistics.

---

## ✨ Key Capabilities

* 🔄 **Triple Threat Processing:** Seamlessly handle live continuous webcam feeds, pre-recorded video files (`.mp4`, `.avi`), and static image uploads.
* 🎯 **Real-Time Object Detection:** Powered by the state-of-the-art **YOLOv8** COCO model to accurately classify, locate, and bound 80+ everyday object classes.
* 🏷️ **Multi-Object Tracking:** Assigns persistent tracking IDs to moving objects across sequential frames for robust motion analysis.
* 📊 **Live Analytics Dashboard:** Features a dynamic web UI complete with real-time FPS monitoring, active detection counters, and unique object tallies updated via asynchronous AJAX polling.
* ⚡ **Multi-Threaded Architecture:** Utilizes dedicated queue streaming to eliminate interface freezes and maintain high frame rates during live webcam execution.

---

## 🛠️ Tech Stack

* **Backend & Routing:** Python, Flask, NumPy
* **Computer Vision & AI:** Ultralytics YOLOv8, OpenCV (`cv2`)
* **Frontend:** HTML5, CSS3, JavaScript (AJAX, DOM manipulation)
* **Architecture:** Modular design with multi-threaded background frame buffering

---

## 📁 Project Structure

```text
CodeAlpha_ObjectDetectionTracking/
│
├── app.py                 # Core Flask application & API routes
├── config.py              # Global configuration parameters & confidence thresholds
├── detection/
│   ├── detector.py        # YOLOv8 wrapper for bounding boxes & tracking algorithms
│   └── annotator.py       # Frame rendering utility for labels, scores, and FPS
│
├── utils/
│   └── video.py           # Multithreaded queue streaming & file I/O fallback
│
├── static/
│   ├── css/               # Dashboard styling
│   └── js/                # Frontend polling & dynamic status updates
│
├── templates/
│   └── index.html         # Main dashboard user interface
│
└── requirements.txt       # Project dependencies
