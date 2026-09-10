import cv2
from ultralytics import YOLO

from config import (
    MODEL_PATH,
    CONFIDENCE,
    VEHICLE_CLASSES,
    GREEN,
    BLUE
)


class VehicleDetector:

    def __init__(self):

        self.model = YOLO(MODEL_PATH)

    def setUseCuda(self):
        self.model.to("cuda")

    def detect(self, frame, queue_region):

        results = self.model.track(
            frame,
            persist=True,
            conf=CONFIDENCE,
            classes=VEHICLE_CLASSES,
            verbose=False,
            device="cuda"
        )

        detections = []


        # =================================================
        # GAMBAR REGION
        # =================================================

        cv2.polylines(
            frame,
            [queue_region],
            True,
            (255, 0, 255),
            3
        )


        # =================================================
        # DETEKSI
        # =================================================

        for result in results:

            if result.boxes is None:
                continue


            for box in result.boxes:

                cls = int(box.cls[0])

                if cls not in VEHICLE_CLASSES:
                    continue


                confidence = float(box.conf[0])


                # =========================================
                # ID TRACKING
                # =========================================

                if box.id is None:
                    continue

                track_id = int(box.id[0])


                # =========================================
                # BOUNDING BOX
                # =========================================

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                # =========================================
                # CENTER POINT
                # =========================================

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)


                # =========================================
                # CEK APAKAH CENTER MASUK REGION
                # =========================================

                inside_region = cv2.pointPolygonTest(
                    queue_region,
                    (cx, cy),
                    False
                )


                # =========================================
                # WARNA
                # =========================================

                if inside_region >= 0:

                    color = GREEN

                else:

                    color = (0, 0, 255)


                # =========================================
                # BOUNDING BOX
                # =========================================

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )


                # =========================================
                # CENTER
                # =========================================

                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    BLUE,
                    -1
                )


                # =========================================
                # LABEL
                # =========================================

                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )


                # =========================================
                # SIMPAN DETEKSI
                # =========================================

                detections.append({

                    "id": track_id,

                    "center": (cx, cy),

                    "inside_region": inside_region >= 0

                })


        return detections, frame