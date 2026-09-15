import cv2
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# Video
cap = cv2.VideoCapture("Screen Recording 2026-09-15 103906.mp4")

# Ambil satu frame dari video
ret, sample_frame = cap.read()
if ret:
    # Simpan frame buat referensi
    cv2.imwrite("Screen Recording 2026-09-15 103906.jpg", sample_frame)
    print("Frame disimpan sebagai sample_frame.jpg")
    print("Buka gambar ini, catat koordinat polygon-nya")
    print("Atau pake kode klik di bawah ini:")