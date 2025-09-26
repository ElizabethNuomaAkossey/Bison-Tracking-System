from nicegui import ui,app
import asyncio
import random
import time
from typing import Dict, Any
from datetime import datetime
import json
import cv2
import requests
import matplotlib.pyplot as plt


# Exposing assets folder
app.add_static_files("/assets","assets")
# Polling target (rtsp_bison_tracker_2.py serves this)
RTSP_STATS_URL = "http://localhost:8000/stats"
RTSP_MJPEG_URL = "http://localhost:8000/mjpeg"
RTSP_HLS_URL = "http://localhost:8000/hls.m3u8"

class BisonTracker:
    def __init__(self):
        # default/dummy state; will be overwritten by live stats when available
        self.current_data = {
            "frame": 0,
            "bison_count": 0,
            "fps": 0.0,
            "total_detections": 0,
            "max_bison_in_frame": 0,
            "timestamp": time.time()
        }
        # UI placeholders (set later)
        self.frame_label = None
        self.count_label = None
        self.fps_label = None
        self.total_label = None
        self.max_label = None
        self.timestamp_label = None
        self.chart_count_label = None

    def format_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    
    def livestream(self):
        ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
        with ui.element("main").classes("w-full h-screen"):
            with ui.element("header").classes("w-full text-balck text-xl shadow-lg justify-between md:px-5 md:py-3 flex items-center inline sticky top-0 bottom-0 z-50 bg-white"):
                with ui.row().classes("justify-center items-center"):
                    ui.image("/assets/bison_logo.png").classes("w-10 h-10")
                    ui.label("Bison Tracker")
                with ui.row():
                    ui.link("Dashboard").classes("no-underline text-black")
                    ui.link("Reports").classes("no-underline text-black")
                    ui.link("Settings").classes("no-underline text-black")
                with ui.row():
                    ui.button(icon='settings').props('flat round size=5').classes("bg-green-200 text-black hover:bg-green-300")
                    ui.button(icon='help').props('flat round').classes("bg-green-200 text-black hover:bg-green-300")
            with ui.element("hero").classes("w-full h-full bg-gray-800"):
                with ui.row().classes('w-full items-center justify-between my-8 px-5'):
                    ui.label('Live Monitoring').classes('text-2xl font-bold text-gray-900 dark:text-white')
                    with ui.row().classes('gap-2'):
                        ui.button('Chart Options', icon='tune').props('flat no-caps').classes("bg-green-200 rounded-lg hover:bg-green-400 text-black dark:text-white font-bold")
                        ui.button('Export', icon='download').props('flat no-caps').classes("bg-green-200 rounded-lg hover:bg-green-300 text-black dark:text-white font-bold")
            
                with ui.row().classes("w-full md:mb-7 md:gap-8 flex flex-wrap"):  # Main row
                    # Left: Video
                    with ui.row().classes("w-full lg:w-[60%] gap-4"):
                        # MJPEG Stream
                        with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[48%]"):
                            ui.label("MJPEG Stream").classes("text-sm font-bold mb-2")
                            ui.html(f'''
                                <img id="mjpeg" src="{RTSP_MJPEG_URL}" 
                                    style="width:100%; height:auto; border-radius:8px; background:#000;"
                                    onerror="this.style.display='none'; document.getElementById('mjpeg_err').style.display='block';" /> 
                                <div id="mjpeg_err" style="display:none;color:#f00;margin-top:6px;">
                                    MJPEG stream not available (check rtsp server)
                                </div>
                                <div style="margin-top:6px">
                                    <button onclick="const i=document.getElementById('mjpeg'); i.src=''; 
                                                    setTimeout(()=>i.src='{RTSP_MJPEG_URL}', 120);">
                                        Refresh MJPEG
                                    </button>
                                </div>
                            ''')

                        # HLS Stream
                        with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[48%]"):
                            ui.label("HLS Stream").classes("text-sm font-bold mb-2")
                            ui.html('''
                                <video id="hlsVideo" controls autoplay muted playsinline 
                                    style="width:100%; max-height:240px; border-radius:8px; background:#000;">
                                </video>
                                <div id="hls_err" style="display:none;color:#f00;margin-top:6px;">
                                    HLS not available yet.
                                </div>
                            ''')
                            # inject the HLS.js loader globally
                            ui.add_body_html(f'''
                                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
                                <script>
                                (function(){{
                                    function tryLoad() {{
                                    fetch('{RTSP_HLS_URL}', {{method:'HEAD', cache:'no-store'}}).then(r=>{{
                                        if (r.status===200) return '{RTSP_HLS_URL}';
                                        throw new Error('playlist not ready');
                                    }}).then(url=>{{
                                        const video = document.getElementById('hlsVideo');
                                        if (window.Hls && Hls.isSupported()) {{
                                        const hls = new Hls();
                                        hls.loadSource(url);
                                        hls.attachMedia(video);
                                        }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                                        video.src = url;
                                        }} else {{
                                        document.getElementById('hls_err').style.display='block';
                                        }}
                                    }}).catch(()=>{{ document.getElementById('hls_err').style.display='block'; }});
                                    }}
                                    setTimeout(tryLoad, 800);
                                }})();
                                </script>
                            ''')

                    
                    # Right: Stacked cards
                    with ui.column().classes("w-full lg:w-[35%] gap-4"):  # Column for two cards
                        # Alerts card
                        with ui.card().classes(" w-full p-4 "):
                            ui.label("Alerts").classes("text-lg ")
                            # Add more content here (e.g., alert list or timestamps)
                        
                        # Bison Count Over Time card
                        with ui.card().classes("p-4 w-full"):
                            ui.label("Bison Count Over Time").classes("text-lg")
                            # line chart
                            self.line_plot = ui.line_plot(n=1, limit=50, figsize=(6, 2), update_every=1).with_legend(['Bison Count'], loc='upper left') 
                        # Bison movement card
                        with ui.card().classes("p-4 w-full"):
                            ui.label("Bison Movement").classes('text-lg')

                # Real-time data cards
        ui.label('Real-Time Data').classes('text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4')

        with ui.element("div").classes('grid grid-cols-2 lg:grid-cols-6 gap-4 w-full'):
            # Frame card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.frame_label = ui.label(str(self.current_data["frame"])) \
                    .classes('text-2xl font-bold text-gray-900 dark:text-white')

            # Bison count card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('Bison Count').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.count_label = ui.label(str(self.current_data["bison_count"])) \
                    .classes('text-2xl font-bold text-gray-900 dark:text-white')

            # FPS card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('FPS').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.fps_label = ui.label(str(self.current_data["fps"])) \
                    .classes('text-2xl font-bold text-gray-900 dark:text-white')

            # Total detections card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('Total Detections').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.total_label = ui.label(str(self.current_data["total_detections"])) \
                    .classes('text-2xl font-bold text-gray-900 dark:text-white')

            # Max in frame card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('Max in Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.max_label = ui.label(str(self.current_data["max_bison_in_frame"])) \
                    .classes('text-2xl font-bold text-gray-900 dark:text-white')

            # Timestamp card
            with ui.card().classes('bg-green-200 p-4'):
                ui.label('Timestamp').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                self.timestamp_label = ui.label(self.format_timestamp(self.current_data["timestamp"])) \
                    .classes('text-lg font-bold text-gray-900 dark:text-white')
                
        # start polling the RTSP server stats via a synchronous timer
        ui.timer(1.0, self.poll_stats_sync)  # runs every 1 second


    def poll_stats_sync(self):
        """Synchronous poll of RTSP server stats endpoint."""
        try:
            resp = requests.get(RTSP_STATS_URL, timeout=0.8)
            if resp.status_code == 200:
                data = resp.json()
                # rtsp script uses keys: total_frames, total_detections, max_bison_in_frame, avg_confidence, fps
                self.current_data["frame"] = int(data.get("total_frames", self.current_data["frame"]))
                # Note: the RTSP server doesn't send the instantaneous bison_count; we will use max_bison_in_frame as proxy,
                # but better if the model publishes per-frame bison_count; we'll use max_bison_in_frame for the big label.
                self.current_data["bison_count"] = int(data.get("max_bison_in_frame", 0))
                self.current_data["fps"] = float(data.get("fps", 0.0))
                self.current_data["total_detections"] = int(data.get("total_detections", 0))
                self.current_data["max_bison_in_frame"] = int(data.get("max_bison_in_frame", 0))
                # update a timestamp
                self.current_data["timestamp"] = time.time()

                # Apply updates to UI DOM via small innerHTML updates (faster than rebuilding labels)
                ui.run_javascript(f"document.getElementById('frame_val').textContent = '{self.current_data['frame']:,}';")
                ui.run_javascript(f"document.getElementById('count_val').textContent = '{self.current_data['bison_count']}';")
                ui.run_javascript(f"document.getElementById('fps_val').textContent = '{self.current_data['fps']:.1f}';")
                ui.run_javascript(f"document.getElementById('total_val').textContent = '{self.current_data['total_detections']:,}';")
                ui.run_javascript(f"document.getElementById('max_val').textContent = '{self.current_data['max_bison_in_frame']}';")
                # big chart label and timestamp
                self.chart_count_label.text = str(self.current_data["bison_count"])
                self.timestamp_label.text = self.format_timestamp(self.current_data["timestamp"])

        except Exception:
            # If any error (server down/unreachable), do a small local fallback: keep previous values or random quick demo
            # Do nothing here so UI retains previous snapshot
            pass

    def run(self, port: int = 8000):
        self.create_ui()
        ui.run(title='Bison Tracker Dashboard', favicon='🦌')


if __name__ in {"__main__", "__mp_main__"}:
    tracker = BisonTracker()
    tracker.run()


tracker = BisonTracker()


@ui.page("/livestream")
def livestream():
    tracker.livestream()

        