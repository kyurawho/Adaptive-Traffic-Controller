import argparse
import time

import cv2
import torch
from ultralytics import YOLO

from config import CONFIDENCE, LOOP_VIDEO, MODEL_OPTIONS, VEHICLE_CLASSES, VIDEO_PATHS


def benchmark_model(model_name, model_path, video_path, frames, warmup, device):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Gagal membuka video: {video_path}")

    processed = 0
    measured = 0
    elapsed = 0.0

    while measured < frames:
        ret, frame = cap.read()
        if not ret:
            if LOOP_VIDEO:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            break

        start = time.perf_counter()
        model.track(
            frame,
            persist=True,
            conf=CONFIDENCE,
            classes=VEHICLE_CLASSES,
            verbose=False,
            device=device,
            tracker="bytetrack.yaml",
        )
        duration = time.perf_counter() - start
        processed += 1

        if processed > warmup:
            measured += 1
            elapsed += duration

    cap.release()
    if measured == 0 or elapsed == 0:
        return model_name, 0.0, 0.0, measured

    fps = measured / elapsed
    avg_ms = (elapsed / measured) * 1000.0
    return model_name, fps, avg_ms, measured


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark FPS YOLO model")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["yolov8n", "yolo26n"],
        help="Daftar model key (contoh: yolov8n yolo26n)",
    )
    parser.add_argument(
        "--video",
        default=VIDEO_PATHS[0],
        help="Path video untuk benchmark",
    )
    parser.add_argument("--frames", type=int, default=300, help="Jumlah frame terukur")
    parser.add_argument("--warmup", type=int, default=30, help="Jumlah frame warmup")
    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        choices=["cpu", "cuda"],
        help="Device inferensi",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Video: {args.video}")
    print(f"Device: {args.device}")
    print(f"Warmup: {args.warmup} frame | Measured: {args.frames} frame")
    print("-" * 62)

    rows = []
    for model_name in args.models:
        model_key = model_name.lower()
        model_path = MODEL_OPTIONS.get(model_key)
        if not model_path:
            print(f"[SKIP] Model tidak dikenal: {model_name}")
            continue
        print(f"Menjalankan benchmark: {model_key} ({model_path})")
        rows.append(
            benchmark_model(
                model_key,
                model_path,
                args.video,
                args.frames,
                args.warmup,
                args.device,
            )
        )

    if not rows:
        print("Tidak ada model valid untuk diuji.")
        return

    print("\nHasil Benchmark")
    print(f"{'Model':<12} {'FPS':>10} {'Avg ms/frame':>15} {'Measured':>12}")
    print("-" * 52)
    for model_name, fps, avg_ms, measured in rows:
        print(f"{model_name:<12} {fps:>10.2f} {avg_ms:>15.2f} {measured:>12}")


if __name__ == "__main__":
    main()
