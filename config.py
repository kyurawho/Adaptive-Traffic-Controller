import numpy as np

# =====================================================
# YOLO MODEL
# =====================================================

MODEL_PATH = "yolo26n.pt"

CONFIDENCE = 0.6

# COCO Classes
# 2 = Car
# 3 = Motorcycle
# 5 = Bus
# 7 = Truck

VEHICLE_CLASSES = [2, 3, 5, 7]


# =====================================================
# VIDEO PATH
# =====================================================

# Untuk sementara 1 video yang sama digunakan
# sebagai 4 simpang

VIDEO_PATHS = [
    "heavy_traffic.mp4",
    "medium_video.mp4",
    "medium_video1.mp4",
    "light_traffic.mp4"
]


# =====================================================
# ENTRY LINE
# =====================================================

# FORMAT:
# ((x1, y1), (x2, y2))

# GANTI KOORDINAT INI SESUAI ENTRY LINE KAMU

# QUEUE_REGIONS = [
#     np.array([[219, 322], [497, 316], [361, 67], [286, 68]], dtype=np.int32)
# ]

HEAVY_REGION = np.array([[250, 400], [850, 400], [1000, 550], [60, 550]], dtype=np.int32)
MEDIUM_REGION = np.array([[200, 500], [580, 500], [550, 620], [30, 620]], dtype=np.int32)
MEDIUM1_REGION = np.array([[39, 76], [381, 76], [710, 280], [60, 280]], dtype=np.int32)
LIGHT_REGION = np.array([[550, 150], [780, 150], [900, 300], [500, 300]], dtype=np.int32)

REGIONS = [HEAVY_REGION, MEDIUM_REGION, MEDIUM1_REGION, LIGHT_REGION]

# =====================================================
# TRAFFIC LIGHT
# =====================================================

# Setiap 1 kendaraan
# mendapatkan tambahan 10 detik green

GREEN_PER_VEHICLE = 10

# Minimum green
MIN_GREEN = 10

# Maximum green
MAX_GREEN = 30

# Durasi kuning
YELLOW_TIME = 3

# Durasi semua merah sebelum pindah
ALL_RED_TIME = 2

JML_KELUAR_PERMENIT = 15

# =====================================================
# DASHBOARD
# =====================================================

VIDEO_WIDTH = 480
VIDEO_HEIGHT = 270

PANEL_WIDTH = 400

WINDOW_WIDTH = VIDEO_WIDTH * 2 + PANEL_WIDTH
WINDOW_HEIGHT = VIDEO_HEIGHT * 2

WINDOW_NAME = "Adaptive Traffic Controller"


# =====================================================
# WARNA
# =====================================================

BLACK = (20, 20, 20)

WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

RED = (0, 0, 255)

YELLOW = (0, 255, 255)

BLUE = (255, 150, 0)

GRAY = (120, 120, 120)


# =====================================================
# FONT
# =====================================================

FONT = 0

FONT_SCALE = 0.7

THICKNESS = 2


# =====================================================
# TITLE
# =====================================================

TITLE = "ADAPTIVE TRAFFIC CONTROLLER"


# =====================================================
# VIDEO LOOP
# =====================================================

LOOP_VIDEO = True