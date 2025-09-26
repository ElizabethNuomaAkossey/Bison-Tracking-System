# #!/usr/bin/env python3
# """
# Headless Bison Tracking Script for Server/Cluster Environment
# Now also logs per-frame stats into a JSON file.
# """

# import os
# import time
# import cv2
# import json   
# import numpy as np
# from ultralytics import YOLO

# # ─── PARAMETERS ────────────────────────────────────────────────────────────────
# VIDEO_SOURCE   = "rtsps://cr-14.hostedcloudvideo.com:443/publish-cr/_definst_/G0W2EP7IKAXYETM1ANDVQ6DBRXNXCN7VK3MM7SP9/6b55ae911a8dbd2bd7d3a75ae4547acc976d0b9e?action=PLAY"   # your RTSP or video file
# OUTPUT_PATH    = "Bison-tracked_new.mp4"
# TRACKER_CFG    = "args.yaml"
# MODEL_WEIGHTS  = "best.pt"
# CLASS_NAMES    = ["bison"]
# MIN_CONFIDENCE = 0.3
# HEADLESS_MODE  = True
# PROGRESS_INTERVAL = 100
# JSON_OUTPUT    = "bison_results.json"   # <<< NEW
# # ──────────────────────────────────────────────────────────────────────────────

# def main():
#     print("=" * 60)
#     print("Headless Bison Tracking with ByteTracker + JSON logging")
#     print("=" * 60)

#     # 1. Load model
#     model = YOLO(MODEL_WEIGHTS)

#     if not os.path.isfile(TRACKER_CFG):
#         raise FileNotFoundError(f"Tracker config not found: {TRACKER_CFG}")

#     # 2. Open video source
#     cap = cv2.VideoCapture(VIDEO_SOURCE)
#     if not cap.isOpened():
#         raise RuntimeError(f"Cannot open source: {VIDEO_SOURCE}")

#     width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # 3. Prepare VideoWriter
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#     writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

#     # 4. Init counters
#     frame_count = 0
#     start_time = time.time()
#     total_bison_detections = 0
#     max_bison_in_frame = 0
#     results_log = []   # <<< NEW: list to store per-frame stats

#     try:
#         while True:
#             loop_start = time.time()
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame_count += 1

#             # Detect + track
#             results = model.track(
#                 source=frame,
#                 tracker=TRACKER_CFG,
#                 conf=MIN_CONFIDENCE,
#                 persist=True,
#                 verbose=False
#             )[0]

#             boxes = results.boxes
#             bison_count = 0

#             if boxes is not None:
#                 coords     = boxes.xyxy.tolist()
#                 cls_list   = boxes.cls.tolist()
#                 ids_tensor = boxes.id
#                 id_list    = ids_tensor.tolist() if ids_tensor is not None else [None]*len(cls_list)
#                 conf_list  = boxes.conf.tolist()

#                 for (x1, y1, x2, y2), tid, cls, conf in zip(coords, id_list, cls_list, conf_list):
#                     cls = int(cls)
#                     if cls >= len(CLASS_NAMES) or CLASS_NAMES[cls] != "bison":
#                         continue
#                     bison_count += 1
#                     x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#             # Update stats
#             total_bison_detections += bison_count
#             max_bison_in_frame = max(max_bison_in_frame, bison_count)
#             fps_display = 1.0 / (time.time() - loop_start + 1e-6)

#             # <<< NEW: Save frame stats into dictionary
#             frame_stats = {
#                 "frame": frame_count,
#                 "bison_count": bison_count,
#                 "fps": round(fps_display, 2),
#                 "total_bison_detections": total_bison_detections,
#                 "max_bison_in_frame": max_bison_in_frame,
#                 "timestamp": time.time()
#             }
#             results_log.append(frame_stats)

#             # Overlay and write
#             cv2.putText(frame, f"Count: {bison_count}", (10, 30),
#                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
#             cv2.putText(frame, f"FPS: {fps_display:.1f}", (width - 140, 30),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
#             cv2.putText(frame, f"Frame: {frame_count}/{total_frames}",
#                        (10, height - 20),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#             writer.write(frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     finally:
#         cap.release()
#         writer.release()
#         cv2.destroyAllWindows()

#         # <<< NEW: Save results log to JSON
#         with open(JSON_OUTPUT, "w") as f:
#             json.dump(results_log, f, indent=2)
#         print(f"→ Saved JSON results to {JSON_OUTPUT}")

# if __name__ == "__main__":
#     main()


# import json
# from nicegui import ui,app
# import datetime

# @ui.page("/livestream")
# def livestream():
#     ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
#     with ui.element("main").classes("w-full h-screen"):
#         # ... (your header code stays the same)

#         with ui.row().classes("w-full h-full md:gap-8 flex flex-wrap"):
#             # Left: Video
#             with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[60%]"):
#                 # Load video player properly (file served from /assets)
#                 ui.html('''
#                     <video src="Bison-tracked_new.mp4" 
#                            controls autoplay muted 
#                            class="w-full h-full rounded-lg shadow">
#                     </video>
#                 ''').style("position: relative; width: 100%; aspect-ratio: 16/9;")

#             # Right: Stats (from JSON)
#             with ui.column().classes("w-full lg:w-[35%] gap-4"):
#                 with open("video_metadata.json") as f:
#                     data = json.load(f)

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("Frame").classes("text-sm font-medium")
#                     ui.label(str(data["frame"])).classes("text-2xl font-bold")

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("Bison Count").classes("text-sm font-medium")
#                     ui.label(str(data["bison_count"])).classes("text-2xl font-bold")

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("FPS").classes("text-sm font-medium")
#                     ui.label(str(round(data["fps"], 2))).classes("text-2xl font-bold")

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("Total Detections").classes("text-sm font-medium")
#                     ui.label(str(data["total_bison_detections"])).classes("text-2xl font-bold")

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("Max in Frame").classes("text-sm font-medium")
#                     ui.label(str(data["max_bison_in_frame"])).classes("text-2xl font-bold")

#                 with ui.card().classes("p-4 w-full"):
#                     ui.label("Timestamp").classes("text-sm font-medium")
#                     ui.label(datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")).classes("text-lg font-bold")
# ui.run()
