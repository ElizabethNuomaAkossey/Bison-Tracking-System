# from nicegui import ui, app
# import asyncio, json, os, time, csv
# from pathlib import Path
# import pandas as pd

# STATIC_DIR = Path('/mnt/data/static')
# JSON_PATH = Path('bison_results.json')
# CONFIG_PATH = Path('session_config.json')

# # -------------------
# # Helpers
# # -------------------
# def read_results():
#     if not JSON_PATH.exists():
#         return []
#     try:
#         with JSON_PATH.open('r') as f:
#             return json.load(f)
#     except Exception:
#         return []

# def read_config():
#     if not CONFIG_PATH.exists():
#         return {}
#     try:
#         with CONFIG_PATH.open('r') as f:
#             return json.load(f)
#     except Exception:
#         return {}

# # -------------------
# # Header component
# # -------------------
# def header():
#     with ui.header().classes('bg-green-700 text-white shadow-sm'):
#         with ui.row().classes('w-full flex items-center justify-between'):
#             with ui.row().classes('items-center gap-4'):
#                 ui.image(str(STATIC_DIR / 'logo.png')).classes('h-10')
#                 ui.label('Bison Guard').classes('text-xl font-semibold')
#             with ui.row().classes('items-center gap-6'):
#                 ui.link('Dashboard', '/dashboard').classes('text-white no-underline hover:underline')
#                 ui.link('Reports', '/reports').classes('text-white no-underline hover:underline')
#                 ui.link('Help', '/help').classes('text-white no-underline hover:underline')
#                 ui.avatar(str(STATIC_DIR / 'user.png')).classes('h-10 w-10')

# # -------------------
# # Home Page
# # -------------------
# @ui.page('/')
# def home_page():
#     header()
#     with ui.column().classes('items-center justify-center gap-6').style('min-height: calc(100vh - 80px);'):
#         ui.image(str(STATIC_DIR / 'landing_bg.jpg')).classes(
#             'w-full max-h-[520px] object-cover rounded-lg shadow-lg'
#         )
#         ui.label('Welcome to Bison Guard').classes('text-3xl font-bold text-green-700')
#         ui.label('Empowering smart animal farming through AI-powered monitoring.').classes('text-lg text-gray-700')

#         with ui.row():
#             def open_form():
#                 form_dialog.open()
#             ui.button('Start Tracking', on_click=open_form).classes(
#                 'bg-green-600 text-white px-6 py-3 rounded-md shadow-md hover:bg-green-700'
#             )

#         # Modal form
#         with ui.dialog() as form_dialog, ui.card().style('min-width:320px;'):
#             ui.label('Start a Tracking Session').classes('text-lg font-medium')
#             rtsp_input = ui.input(
#                 'RTSP / Video URL',
#                 placeholder='rtsp://... or /path/to/sample.mp4'
#             ).props('autofocus')

#             mode = ui.select(
#                 ['Apply bison detection model (requires model files)',
#                  'Stream only (no AI processing)'],
#                 label='Processing option',
#                 value='Apply bison detection model (requires model files)'
#             )

#             def submit():
#                 config = {
#                     'url': rtsp_input.value or 'Bison-tracked_new.mp4',
#                     'mode': mode.value,
#                     'started_at': time.time()
#                 }
#                 with CONFIG_PATH.open('w') as f:
#                     json.dump(config, f)
#                 ui.notify('Session saved. Now run tracker.py to start detection.', color='positive')
#                 form_dialog.close()
#                 ui.navigate.to('/dashboard')

#             with ui.row().classes('justify-end gap-2 mt-4'):
#                 ui.button('Cancel', on_click=lambda: form_dialog.close())
#                 ui.button('Start', on_click=submit).classes('bg-green-600 text-white')

# # -------------------
# # Help Page
# # -------------------
# @ui.page('/help')
# def help_page():
#     header()
#     with ui.card().classes('m-6 p-6'):
#         ui.label('Help & Getting Started').classes('text-2xl font-semibold text-green-700')
#         ui.markdown("""
# ### Quick Start
# 1. Click **Start Tracking** on the homepage.  
# 2. Enter your RTSP URL (or path to a video).  
# 3. Choose whether to apply the bison detection model or just stream.  
# 4. Submit → run your `tracker.py` with the same video/RTSP.  
# 5. Open the **Dashboard** to view detections in real-time.

# ### Navigation
# - **Dashboard**: Live monitoring & alerts  
# - **Reports**: Historical analytics & downloads  
# - **Help**: Usage instructions  

# ### Tips
# - Convert RTSP to HLS for browser playback (via `ffmpeg`).  
# - Place your model files in the expected directory if selecting detection mode.  
# - If things don’t update, check `bison_results.json`.
# """)

# # -------------------
# # Dashboard Page
# # -------------------
# @ui.page('/dashboard')
# def dashboard_page():
#     header()
#     session = read_config()

#     with ui.row().classes('m-6 gap-6'):
#         with ui.column().classes('w-2/3'):
#             ui.label('Live Bison Monitoring').classes('text-2xl font-semibold text-green-700')

#             # Video box
#             if session.get('url') and Path(session['url']).exists() and str(session['url']).endswith('.mp4'):
#                 ui.video(session['url']).props('controls autoplay muted playsinline').classes('w-full rounded shadow-md')
#             else:
#                 ui.image(str(STATIC_DIR / 'landing_bg.jpg')).classes('w-full rounded shadow-md')

#             # Alerts
#             alert_label = ui.label('No alerts').classes('text-sm text-red-600 mt-2')

#         with ui.column().classes('w-1/3'):
#             ui.label('Real-time Analytics').classes('text-lg font-medium')
#             count_card = ui.card().classes('p-4 bg-gray-50 shadow-md')

#             with ui.column().classes('w-1/3'):
#                 ui.label('Real-time Analytics').classes('text-lg font-medium')

#                 # Cards for stats
#                 count_card = ui.card().classes('p-4').bind_text('')

#                 # Line plot for bison count over time
#                 line_plot = ui.line_plot(n=1, limit=40, figsize=(4, 3), update_every=1) \
#                             .with_legend(['Bison Count'], loc='upper right', ncol=1)

#                 # Alert label
#                 alert_label = ui.label('No alerts').classes('text-sm text-red-600')

#             # Update loop: poll JSON file every second
#             async def updater():
#                 while True:
#                     data = read_results()
#                     if data:
#                         latest = data[-1]

#                         # Update card
#                         count_card.set_content(
#                             f'<div><b>Current Count:</b> {latest.get("bison_count", 0)}</div>'
#                             f'<div><b>FPS:</b> {latest.get("fps", 0):.1f}</div>'
#                             f'<div><b>Total Detections:</b> {latest.get("total_bison_detections", 0)}</div>'
#                             f'<div><b>Max in Frame:</b> {latest.get("max_bison_in_frame", 0)}</div>'
#                         )

#                         # Push new data point to line plot
#                         frame_num = latest.get('frame', 0)
#                         count = latest.get('bison_count', 0)
#                         timestamp = datetime.fromtimestamp(latest.get('timestamp', time.time()))
#                         line_plot.push([timestamp], [[count]])

#                         # Simple alert
#                         if count >= 5:
#                             alert_label.set_text('ALERT: High bison density detected!')
#                         else:
#                             alert_label.set_text('No alerts')

#                     await asyncio.sleep(1)

#         # ui.run_coroutine(updater())

#             with ui.row().classes('mt-4 gap-2'):
#                 def download_csv():
#                     data = read_results()
#                     if not data:
#                         ui.notify('No data to export', color='warning')
#                         return
#                     df = pd.DataFrame(data)
#                     csv_path = '/mnt/data/bison_export.csv'
#                     df.to_csv(csv_path, index=False)
#                     ui.download(csv_path)

#                 def download_json():
#                     if not JSON_PATH.exists():
#                         ui.notify('No data file found', color='warning')
#                         return
#                     ui.download(str(JSON_PATH))

#                 ui.button('Download CSV', on_click=download_csv).classes('bg-green-700 text-white')
#                 ui.button('Download JSON', on_click=download_json).classes('bg-gray-600 text-white')

#     async def updater():
#         while True:
#             data = read_results()
#             if data:
#                 latest = data[-1]
#                 count_card.set_content(
#                     f"<div><b>Current Count:</b> {latest.get('bison_count',0)}</div>"
#                     f"<div><b>FPS:</b> {latest.get('fps',0)}</div>"
#                     f"<div><b>Total Detections:</b> {latest.get('total_bison_detections',0)}</div>"
#                     f"<div><b>Max in Frame:</b> {latest.get('max_bison_in_frame',0)}</div>"
#                 )
#                 xs = [str(d.get('frame')) for d in data[-40:]]
#                 ys = [d.get('bison_count',0) for d in data[-40:]]
#                 chart.update({'Bison Count': list(zip(xs, ys))})

#                 if latest.get('bison_count',0) >= 5:
#                     alert_label.set_text('ALERT: High bison density detected!')
#                 else:
#                     alert_label.set_text('No alerts')
#             await asyncio.sleep(1)

#     ui.run_coroutine(updater())

# # -------------------
# # Reports Page
# # -------------------
# @ui.page('/reports')
# def reports_page():
#     header()
#     with ui.column().classes('m-6 gap-4'):
#         ui.label('Analytics & Reporting').classes('text-2xl font-semibold text-green-700')
#         ui.markdown('Filter time ranges and export summary reports.')

#         with ui.row().classes('gap-4'):
#             start_input = ui.input('Start frame (optional)')
#             end_input = ui.input('End frame (optional)')

#             def generate_report():
#                 data = read_results()
#                 if not data:
#                     ui.notify('No data available', color='warning')
#                     return
#                 s = int(start_input.value) if start_input.value and start_input.value.isdigit() else 1
#                 e = int(end_input.value) if end_input.value and end_input.value.isdigit() else len(data)
#                 s = max(1, s); e = min(len(data), e)
#                 subset = data[s-1:e]
#                 df = pd.DataFrame(subset)
#                 summary = {
#                     'frames': len(subset),
#                     'total_detections': int(df['bison_count'].sum()),
#                     'max_in_frame': int(df['bison_count'].max()),
#                     'avg_per_frame': float(df['bison_count'].mean())
#                 }
#                 csv_path = '/mnt/data/report_subset.csv'
#                 df.to_csv(csv_path, index=False)
#                 ui.notify(f"Report ready: {summary}", color='positive')
#                 ui.download(csv_path)

#             ui.button('Generate & Download Report', on_click=generate_report).classes('bg-green-700 text-white')

# # -------------------
# # Run app
# # -------------------
# if __name__ == '__main__':
#     ui.run(title='Bison Guard', port=5000, reload=False)

from nicegui import ui,app
from bison_tracker_homepage import *
from bison_tracker_livestream import *
from app import *


ui.run()


