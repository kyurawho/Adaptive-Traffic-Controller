import argparse
import csv
import os
import time
from datetime import datetime

import cv2


def parse_args():
    parser = argparse.ArgumentParser(description="Adaptive Traffic Controller")
    parser.add_argument(
        "--model",
        choices=["yolov8n", "yolo26n"],
        help="Model YOLO yang dipakai",
    )
    parser.add_argument(
        "--video",
        type=int,
        choices=[1, 2, 3, 4],
        help="Nomor video (1-4) untuk mode eksperimen",
    )
    parser.add_argument(
        "--experiment",
        choices=["30s", "10", "30"],
        help="Mode eksperimen: 30 detik, 10 kendaraan real, atau 30 kendaraan real",
    )
    args = parser.parse_args()
    if args.experiment and args.video is None:
        parser.error("--video wajib diisi saat menggunakan --experiment")
    return args


def append_experiment_result(row, output_path):
    file_exists = os.path.exists(output_path)
    with open(output_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "timestamp",
                "model",
                "video",
                "experiment",
                "manual_real_vehicles",
                "detected_vehicles",
                "elapsed_seconds",
                "status",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def run_dashboard_mode(video_paths, processImage, trafficController, TrafficTimer, Dashboard, window_name):
    videonumber = 4
    controller = trafficController()
    trafficTimer = TrafficTimer(controller)
    trafficTimer.Start()
    dashboard = Dashboard()

    processors = []
    for i in range(0, videonumber):
        cap = cv2.VideoCapture(video_paths[i])
        if not cap.isOpened():
            print(f"Gagal membuka video : {video_paths[i]}")
            trafficTimer.Stop()
            return
        process = processImage(cap, i, video_paths[i])
        processors.append(process)

    controller.startController()
    while True:
        frames = []
        frameproblem = False
        for i in range(0, videonumber):
            process: processImage = processors[i]
            try:
                detections, frame = process.processFrame()
                if (frame is not None) and (detections is not None):
                    frames.append(frame)
                    entered_ids = controller.update(detections, i)
                    for vehicle_id in entered_ids:
                        print(f"Vehicle ID {vehicle_id} entered queue region")
                else:
                    frameproblem = True
            except Exception:
                frameproblem = True
        if not frameproblem:
            screen = dashboard.drawDashboard(frames, controller)
            cv2.imshow(window_name, screen)
        else:
            frameproblem = False
        key = cv2.waitKey(1)
        if key == 27:
            break

    trafficTimer.Stop()
    for process in processors:
        process.cap.release()
    cv2.destroyAllWindows()


def run_experiment_mode(args, video_paths, processImage, active_model_name):
    video_index = args.video - 1
    video_path = video_paths[video_index]
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Gagal membuka video : {video_path}")
        return

    processor = processImage(cap, video_index, video_path)
    manual_count = 0
    detected_ids = set()
    start_time = time.perf_counter()
    status = "completed"

    if args.experiment == "30s":
        print("Eksperimen 30 detik dimulai.")
    else:
        print(
            f"Eksperimen {args.experiment} kendaraan real dimulai. "
            "Tekan tombol M setiap kali 1 kendaraan real lewat region."
        )
    print("Tekan ESC untuk menghentikan eksperimen lebih awal.")

    while True:
        detections, frame = processor.processFrame()
        if frame is None or detections is None:
            status = "stopped_no_frame"
            break

        for detection in detections:
            if detection["inside_region"]:
                detected_ids.add(detection["id"])

        elapsed = time.perf_counter() - start_time
        target = None if args.experiment == "30s" else int(args.experiment)
        if args.experiment == "30s" and elapsed >= 30:
            break
        if target is not None and manual_count >= target:
            break

        info_lines = [
            f"Model: {active_model_name}",
            f"Video: {args.video}",
            f"Experiment: {args.experiment}",
            f"Manual real count (M): {manual_count}",
            f"Detected vehicles: {len(detected_ids)}",
            f"Elapsed: {elapsed:.1f}s",
        ]
        y = 20
        for line in info_lines:
            cv2.putText(
                frame,
                line,
                (10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2,
            )
            y += 24

        cv2.imshow("Experiment Mode", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("m"):
            manual_count += 1
        elif key == 27:
            status = "stopped_by_user"
            break

    elapsed_total = time.perf_counter() - start_time
    processor.cap.release()
    cv2.destroyAllWindows()

    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "model": active_model_name,
        "video": args.video,
        "experiment": args.experiment,
        "manual_real_vehicles": manual_count,
        "detected_vehicles": len(detected_ids),
        "elapsed_seconds": round(elapsed_total, 2),
        "status": status,
    }
    append_experiment_result(result, "experiment_results.csv")

    print("\n=== HASIL EKSPERIMEN ===")
    print(f"Model                : {result['model']}")
    print(f"Video                : {result['video']}")
    print(f"Kondisi eksperimen   : {result['experiment']}")
    print(f"Real vehicles manual : {result['manual_real_vehicles']}")
    print(f"Detected vehicles    : {result['detected_vehicles']}")
    print(f"Elapsed seconds      : {result['elapsed_seconds']}")
    print(f"Status               : {result['status']}")
    print("Hasil disimpan ke experiment_results.csv")


def main():
    args = parse_args()
    if args.model:
        os.environ["YOLO_MODEL"] = args.model.lower()

    from config import ACTIVE_MODEL_NAME, VIDEO_PATHS, WINDOW_NAME
    from dashboard import Dashboard
    from detector import processImage
    from region_counter import TrafficTimer, trafficController

    if args.experiment:
        run_experiment_mode(args, VIDEO_PATHS, processImage, ACTIVE_MODEL_NAME)
    else:
        run_dashboard_mode(
            VIDEO_PATHS,
            processImage,
            trafficController,
            TrafficTimer,
            Dashboard,
            WINDOW_NAME,
        )


if __name__ == "__main__":
    main()