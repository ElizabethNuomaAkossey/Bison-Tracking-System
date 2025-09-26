from nicegui import ui, app
import aiohttp
import asyncio
from datetime import datetime
import plotly.graph_objects as go
from collections import deque

# --- Endpoints ---
STATS_URL = "http://localhost:8080/stats"
RTSP_MJPEG_URL = "http://localhost:8080/mjpeg"
RTSP_HLS_URL = "http://localhost:8080/hls.m3u8"

# ByteTrack thresholds for movement
TRACK_HIGH_THRESH = 0.25  # moving
TRACK_LOW_THRESH = 0.10   # grazing

# --- Dashboard Logic ---
class BisonDashboard:
    def __init__(self):
        self.current_data = {
            "total_frames": 0,
            "total_detections": 0,
            "max_bison_in_frame": 0,
            "avg_confidence": 0.0,
            "fps": 0,
            "bison_count": 0,
            "timestamp": ""
        }

    async def poll_stats(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(STATS_URL, timeout=1) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            for key in self.current_data:
                                self.current_data[key] = data.get(key, self.current_data[key])
                except Exception as e:
                    print(f"⚠️ Failed to fetch stats: {e}")
                await asyncio.sleep(1)

dashboard = BisonDashboard()

# Buffers for plots
timestamps = deque(maxlen=20)
bison_counts = deque(maxlen=20)

# ---------------- MOVEMENT CALCULATION ----------------
def compute_movement(avg_confidence, bison_count):
    moving = int(avg_confidence >= TRACK_HIGH_THRESH) * bison_count
    grazing = int(TRACK_LOW_THRESH <= avg_confidence < TRACK_HIGH_THRESH) * bison_count
    stationary = int(avg_confidence < TRACK_LOW_THRESH) * bison_count
    return {"moving": moving, "grazing": grazing, "stationary": stationary}

# --- UI Page ---
@ui.page("/livestream")
def livestream():
    ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
    with ui.element("main").classes("w-full h-screen"):

        # ---------------- HEADER ----------------
        with ui.element("header").classes(
            "w-full text-black text-xl shadow-lg justify-between md:px-5 md:py-3 "
            "flex items-center inline sticky top-0 bottom-0 z-50 bg-white"
        ):
            with ui.row().classes("justify-center items-center"):
                ui.image("/assets/bison_logo.png").classes("w-10 h-10")
                ui.label("Bison Tracker")
            with ui.row():
                ui.link("Dashboard").classes("no-underline text-black")
                ui.link("Reports").classes("no-underline text-black")
                ui.link("Settings").classes("no-underline text-black")
            with ui.row():
                ui.button(icon='settings').props('flat round size=5').classes(
                    "bg-green-200 text-black hover:bg-green-300"
                )
                ui.button(icon='help').props('flat round').classes(
                    "bg-green-200 text-black hover:bg-green-300"
                )

        # ---------------- HERO ----------------
        with ui.element("hero").classes("w-full h-full bg-gray-800"):
            with ui.row().classes('w-full items-center justify-between my-8 px-5'):
                ui.label('Live Monitoring').classes(
                    'text-2xl font-bold text-gray-900 dark:text-white'
                )

            with ui.row().classes("w-full md:h-full md:gap-8 flex flex-wrap"):

                # ---------------- LEFT: VIDEO ----------------
                with ui.row().classes("w-full lg:w-[60%] gap-4"):

                    # MJPEG Stream
                    with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[47%]"):
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
                    with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[47%]"):
                        ui.label("HLS Stream").classes("text-sm font-bold mb-2")
                        ui.html('''
                            <video id="hlsVideo" controls autoplay muted playsinline 
                                style="width:100%; max-height:240px; border-radius:8px; background:#000;">
                            </video>
                            <div id="hls_err" style="display:none;color:#f00;margin-top:6px;">
                                HLS not available yet.
                            </div>
                        ''')
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

                # ---------------- RIGHT: CARDS ----------------
                with ui.column().classes("w-full lg:w-[35%] gap-4"):
                    with ui.card().classes("p-4 w-full"):
                        ui.label("Bison Count Over Time").classes("text-lg")
                        bison_count_fig = go.Figure()
                        bison_count_fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', name='Bison Count'))
                        bison_count_chart = ui.plotly(bison_count_fig).classes("w-full h-64")

                    with ui.card().classes("p-4 w-full"):
                        ui.label("Bison Movement").classes('text-lg')
                        movement_fig = go.Figure()
                        movement_fig.add_trace(go.Pie(labels=["moving","stationary","grazing"], values=[0,0,0]))
                        movement_chart = ui.plotly(movement_fig).classes("w-full h-64")

            # ---------------- GRID STATS ----------------
            with ui.element("div").classes('grid grid-cols-2 lg:grid-cols-6 gap-4 w-full lg:mt-10'):
                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('Frames')
                    frame_label = ui.label("0").classes('text-2xl font-bold')

                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('Total Detections')
                    detections_label_grid = ui.label("0").classes('text-2xl font-bold')

                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('FPS')
                    fps_label = ui.label("0").classes('text-2xl font-bold')

                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('Max in Frame')
                    max_bison_label = ui.label("0").classes('text-2xl font-bold')

                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('Avg Confidence')
                    confidence_label = ui.label("0.00").classes('text-2xl font-bold')

                with ui.card().classes('bg-green-200 p-4'):
                    ui.label('Last Update')
                    timestamp_label = ui.label("--:--:--").classes('text-2xl font-bold')

    # ---------------- UPDATE LOOP ----------------
    async def update_ui():
        while True:
            data = dashboard.current_data
            frame_label.set_text(str(data['total_frames']))
            detections_label_grid.set_text(str(data['total_detections']))
            max_bison_label.set_text(str(data['max_bison_in_frame']))
            confidence_label.set_text(f"{data['avg_confidence']:.2f}")
            fps_label.set_text(str(data['fps']))
            timestamp_label.set_text(data.get("timestamp","--:--:--"))

            # Update Bison Count Over Time
            timestamps.append(data.get("timestamp", datetime.now().strftime("%H:%M:%S")))
            bison_counts.append(data["bison_count"])
            bison_count_chart.figure.data[0].x = list(timestamps)
            bison_count_chart.figure.data[0].y = list(bison_counts)
            bison_count_chart.update()

            # Update Movement Pie Chart
            movement_counts = compute_movement(data['avg_confidence'], data['bison_count'])
            movement_chart.figure.data[0].labels = list(movement_counts.keys())
            movement_chart.figure.data[0].values = list(movement_counts.values())
            movement_chart.update()

            await asyncio.sleep(1)


# --- Serve static assets ---
app.add_static_files("/assets", "assets")

ui.run(port=8000)
