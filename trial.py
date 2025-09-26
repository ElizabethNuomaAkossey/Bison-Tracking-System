# bison_dashboard.py
import time
import random
import requests
from datetime import datetime
from nicegui import ui, app

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

    def create_ui(self):
        ui.add_head_html('''
            <style>
                .video-placeholder { aspect-ratio: 16/9; border-radius: 8px; overflow: hidden; background: #000; }
                .stats-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; }
                .stat { padding:8px; background:#f3f4f6; border-radius:6px; }
            </style>
        ''')

        # Page header
        with ui.header().classes('bg-white/80 backdrop-blur-sm border-b'):
            with ui.row().classes('w-full items-center justify-between px-6 py-3'):
                with ui.row().classes('items-center gap-4'):
                    ui.html('<svg class="h-6 w-6" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M4 4H17.3334V17.3334H30.6666V30.6666H44V44H4V4Z" fill="currentColor"></path></svg>')
                    ui.label('Bison Tracker').classes('text-xl font-bold')
                with ui.row().classes('items-center gap-4'):
                    ui.button(icon='settings').props('flat round').on('click', lambda _: ui.notify('Settings'))
                    ui.button(icon='help').props('flat round').on('click', lambda _: ui.notify('Help'))

        # Main content
        with ui.column().classes('px-6 py-6'):
            with ui.row().classes('items-center justify-between mb-4'):
                ui.label('Live Monitoring').classes('text-2xl font-bold')
                with ui.row().classes('gap-2').props('inline'):
                    ui.button('Chart Options', icon='tune').props('flat')
                    ui.button('Export', icon='download').props('flat')

            # Streams + stats
            with ui.row().classes('gap-6'):
                # Left: Video stream card
                with ui.card().classes('w-full lg:w-2/3'):
                    ui.label('Live Stream').classes('text-lg font-medium')
                    # MJPEG img (auto-refresh button added)
                    self.mjpeg_img = ui.html(f'''<img id="mjpeg" src="{RTSP_MJPEG_URL}" style="width:100%; height:auto; border-radius:6px; background:#000;" onerror="this.style.display='none'; document.getElementById('mjpeg_err').style.display='block';" /> 
                                                <div id="mjpeg_err" style="display:none;color:#f00;margin-top:6px;">MJPEG stream not available (check rtsp server)</div>
                                                <div style="margin-top:6px"><button onclick="const i=document.getElementById('mjpeg'); i.src=''; setTimeout(()=>i.src='{RTSP_MJPEG_URL}', 120);">Refresh MJPEG</button></div>''')
                    ui.add_body_html(f'''
                        <div style="margin-top:12px">
                            <video id="hlsVideo" controls autoplay muted playsinline style="width:100%; max-height:480px; border-radius:6px;"></video>
                            <div id="hls_err" style="display:none;color:#f00;margin-top:6px;">HLS not available yet.</div>
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
                        </div>
                    ''')

                # Right: small stats summary
                with ui.card().classes('w-full lg:w-1/3'):
                    ui.label('Summary').classes('text-lg font-medium')
                    self.chart_count_label = ui.label('0').classes('text-4xl font-bold')
                    with ui.row().classes('items-center gap-2 mt-1'):
                        ui.label('Last update:').classes('text-sm')
                        self.timestamp_label = ui.label(self.format_timestamp(time.time())).classes('text-sm')
                    ui.separator()
                    with ui.element('div').classes('stats-grid mt-2'):
                        self.frame_label = ui.html('<div class="stat"><div class="val" id="frame_val">0</div><div class="lbl">Frame</div></div>')
                        self.count_label = ui.html('<div class="stat"><div class="val" id="count_val">0</div><div class="lbl">Bison Count</div></div>')
                        self.fps_label = ui.html('<div class="stat"><div class="val" id="fps_val">0.0</div><div class="lbl">FPS</div></div>')
                        self.total_label = ui.html('<div class="stat"><div class="val" id="total_val">0</div><div class="lbl">Total Detections</div></div>')
                        self.max_label = ui.html('<div class="stat"><div class="val" id="max_val">0</div><div class="lbl">Max / Frame</div></div>')

            ui.label('Detailed Live Data').classes('text-xl font-bold mt-6')

            # Line plot: 1 line (bison count over time), limit to last 50 points
            self.line_plot = ui.line_plot(n=1, limit=50, figsize=(6, 2), update_every=1) \
                .with_legend(['Bison Count'], loc='upper left')

        # start polling the RTSP server stats via a synchronous timer
        ui.timer(1.0, self.poll_stats_sync)  # runs every 1 second

    def poll_stats_sync(self):
        """Synchronous poll of RTSP server stats endpoint."""
        try:
            resp = requests.get(RTSP_STATS_URL, timeout=0.8)
            if resp.status_code == 200:
                data = resp.json()
                # rtsp script uses keys: total_frames, total_detections, max_bison_in_frame, avg_confidence, fps
                # We'll map those into our UI fields
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
