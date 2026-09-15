import cv2

from config import (
    VIDEO_PATHS,
    LOOP_VIDEO,
    REGIONS,
    WINDOW_NAME
)

from detector import processImage
#from region_counter import RegionCounter
#from traffic_controller import TrafficController
from region_counter import trafficController, TrafficTimer
from dashboard import Dashboard

# ==========================================
# LOAD COMPONENT
# ==========================================
videonumber = 4
#detector = VehicleDetector()
#detector.setUseCuda()

#counter = RegionCounter()

controller = trafficController()
trafficTimer = TrafficTimer(controller)
trafficTimer.Start()

dashboard = Dashboard()


# ==========================================
# VIDEO
# ==========================================
processors = []
for i in range(0, videonumber) :
    cap = cv2.VideoCapture(VIDEO_PATHS[i])
    if not cap.isOpened():
        print(f"Gagal membuka video : {VIDEO_PATHS[i]}")
        exit()
    else :
        process = processImage(cap, i, VIDEO_PATHS[i])
        processors.append(process)
controller.startController()
# ==========================================
# MAIN LOOP
# ==========================================
while True:
    frames = []
    frameproblem = False
    for i in range(0, videonumber):
        process : processImage = processors[i]
        try :
            detections, frame = process.processFrame()
            if (frame is not None) and (detections is not None):
                frames.append(frame)
                entered_ids = controller.update(detections, i)
                for vehicle_id in entered_ids:
                    print(f"Vehicle ID {vehicle_id} " f"entered queue region")
            else :
                frameproblem = True
        except:
            frameproblem = True
    if not frameproblem :
        screen = dashboard.drawDashboard(frames, controller)
        cv2.imshow(WINDOW_NAME, screen)
    else:
        frameproblem = False
    key = cv2.waitKey(1)
    if key == 27:
        break

# ==========================================
# RELEASE
# ==========================================
trafficTimer.Stop()

for i in range (0, videonumber) :
    process = processors[i]
    process.cap.release()

cv2.destroyAllWindows()