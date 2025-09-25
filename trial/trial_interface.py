import asyncio
import random
import time
from typing import Dict, Any
from nicegui import ui, app
from datetime import datetime

class BisonTracker:
    def __init__(self):
        self.current_data = {
            "frame": 12345,
            "bison_count": 15,
            "fps": 30,
            "total_bison_detections": 5000,
            "max_bison_in_frame": 20,
            "timestamp": time.time()
        }
        self.is_dark_mode = False
        self.chart_svg = '''
            <svg fill="none" height="100%" preserveAspectRatio="none" viewBox="0 0 472 150" width="100%" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient gradientUnits="userSpaceOnUse" id="chartGradient" x1="0" x2="0" y1="0" y2="150">
                        <stop stop-color="#54cf17" stop-opacity="0.3"></stop>
                        <stop offset="1" stop-color="#54cf17" stop-opacity="0"></stop>
                    </linearGradient>
                </defs>
                <path d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25V150H0V109Z" fill="url(#chartGradient)"></path>
                <path d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25" stroke="#54cf17" stroke-linecap="round" stroke-width="3"></path>
            </svg>
        '''

    def format_timestamp(self, timestamp: float) -> str:
        """Format timestamp to HH:MM:SS"""
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        ui.run_javascript(f'''
            document.documentElement.classList.toggle('dark', {str(self.is_dark_mode).lower()});
        ''')

    async def update_data(self):
        """Simulate real-time data updates"""
        while True:
            # Simulate new data (replace with actual detection data)
            self.current_data.update({
                "frame": self.current_data["frame"] + random.randint(1, 5),
                "bison_count": random.randint(1, 25),
                "fps": random.randint(25, 35),
                "total_bison_detections": self.current_data["total_bison_detections"] + random.randint(0, 3),
                "max_bison_in_frame": max(self.current_data["max_bison_in_frame"], random.randint(1, 30)),
                "timestamp": time.time()
            })
            
            # Update UI elements
            self.update_ui_elements()
            await asyncio.sleep(2)  # Update every 2 seconds

    def update_ui_elements(self):
        """Update all UI elements with new data"""
        # Update chart count
        self.chart_count_label.text = str(self.current_data["bison_count"])
        
        # Update data cards
        self.frame_label.text = str(self.current_data["frame"])
        self.count_label.text = str(self.current_data["bison_count"])
        self.fps_label.text = str(self.current_data["fps"])
        self.total_label.text = str(self.current_data["total_bison_detections"])
        self.max_label.text = str(self.current_data["max_bison_in_frame"])
        self.timestamp_label.text = self.format_timestamp(self.current_data["timestamp"])

    def create_ui(self):
        """Create the main UI"""
        # Add custom CSS for styling
        ui.add_head_html('''
            <link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;700;900&display=swap" rel="stylesheet">
            <style>
                :root {
                    --primary-color: #54cf17;
                    --bg-light: #f6f8f6;
                    --bg-dark: #162111;
                }
                
                body {
                    font-family: 'Public Sans', sans-serif !important;
                    background-color: var(--bg-light);
                    color: #374151;
                }
                
                .dark body {
                    background-color: var(--bg-dark);
                    color: #e5e7eb;
                }
                
                .primary-text { color: var(--primary-color) !important; }
                .primary-bg { background-color: rgba(84, 207, 23, 0.1) !important; }
                .primary-bg-20 { background-color: rgba(84, 207, 23, 0.2) !important; }
                .primary-border { border-color: rgba(84, 207, 23, 0.2) !important; }
                
                .dark .primary-bg { background-color: rgba(84, 207, 23, 0.2) !important; }
                .dark .primary-bg-20 { background-color: rgba(84, 207, 23, 0.3) !important; }
                
                .card-bg {
                    background-color: var(--bg-light);
                    border: 1px solid rgba(84, 207, 23, 0.2);
                }
                
                .dark .card-bg {
                    background-color: var(--bg-dark);
                }
                
                .video-placeholder {
                    background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuD5QtQaVZRZtHo5BHk8KcLZO637V8lOTjMxjqatVvpDSZQvocx9jbEN8SBFcNEh8iBymQLEP3IwcDrnxNTb25CNFwxCHVKynV69i_IVYcXrJcA9aKhClhS3olSZYRroH9S25_c424YmQvfeD13Z94gXOGMySW-qprf78cSaEO1pbosgZPRE34mC0IAiZS2xyxvs5r3mL-6z0Ff2waVC44mNGBrOTJmCjsN-liEJRwuz2Gq51t53Tij03MrsvVqzio-x_0H0KlRutSE');
                    background-size: cover;
                    background-position: center;
                    aspect-ratio: 16/9;
                    border-radius: 0.75rem;
                    position: relative;
                }
                
                .play-button {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 80px;
                    height: 80px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    backdrop-filter: blur(4px);
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                
                .play-button:hover {
                    transform: translate(-50%, -50%) scale(1.1);
                }
                
                .chart-container {
                    height: 160px;
                    width: 100%;
                }
            </style>
        ''')

        # Header
        with ui.header().classes('bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b primary-border'):
            with ui.row().classes('w-full items-center justify-between px-10 py-3'):
                # Logo and title
                with ui.row().classes('items-center gap-4'):
                    ui.html('''
                        <svg class="h-6 w-6 primary-text" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4 4H17.3334V17.3334H30.6666V30.6666H44V44H4V4Z" fill="currentColor"></path>
                        </svg>
                    ''')
                    ui.label('Bison Tracker').classes('text-xl font-bold text-gray-900 dark:text-white')
                
                # Navigation
                with ui.row().classes('hidden md:flex items-center gap-8'):
                    ui.link('Dashboard', '#').classes('text-sm font-medium text-gray-700 hover:primary-text dark:text-gray-300')
                    ui.link('Reports', '#').classes('text-sm font-medium text-gray-700 hover:primary-text dark:text-gray-300')
                    ui.link('Settings', '#').classes('text-sm font-medium text-gray-700 hover:primary-text dark:text-gray-300')
                
                # Action buttons
                with ui.row().classes('items-center gap-4'):
                    ui.button(icon='settings', on_click=self.toggle_dark_mode).props('flat round').classes('primary-bg hover:primary-bg-20')
                    ui.button(icon='help', on_click=lambda: ui.notify('Help clicked')).props('flat round').classes('primary-bg hover:primary-bg-20')
                    ui.avatar().props('size=40px').style('background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBTmSPQSSVXBEjEvoykPqA7JglyrJVD4-lJUt1QJV9xTwl3g52H0jXEw2alRjD9C55NhrhAR-9qWp-0XBy3mJQnHZqj6dH_qPqm8_e9VH0pKIIOPv0SJkRaza4jN7iKXPjKcTcBYQah16zgb3MD_PiSt_OJI0xZ5C8GGFAVUXXGWI40APqwlR6zKEki6IIOqj3bZL3LyDsi6WsO2aaXbhmZ9Br5mjbfadCuQ7BUBp9ES3Nz7Egi9Y1ujAfJGgAAy85-p0KyC8U81hU"); background-size: cover;')

        # Main content
        with ui.column().classes('flex-1 px-4 py-8 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full'):
            # Title and buttons
            with ui.row().classes('w-full items-center justify-between mb-8'):
                ui.label('Live Monitoring').classes('text-3xl font-bold text-gray-900 dark:text-white')
                with ui.row().classes('gap-2'):
                    ui.button('Chart Options', icon='tune').classes('primary-bg-20 hover:primary-bg text-gray-800 dark:text-white font-bold')
                    ui.button('Export', icon='download').classes('primary-bg-20 hover:primary-bg text-gray-800 dark:text-white font-bold')

            # Video and Chart Grid
            with ui.grid(columns=3).classes('w-full gap-8'):
                # Video player (spans 2 columns)
                with ui.column().classes('col-span-3 lg:col-span-2'):
                    with ui.card().classes('video-placeholder shadow-lg'):
                        ui.html('''
                            <div class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                                <div class="play-button">
                                    <svg width="48" height="48" fill="white" viewBox="0 0 24 24">
                                        <path d="M8 5v14l11-7z"/>
                                    </svg>
                                </div>
                            </div>
                        ''').style('position: relative; width: 100%; aspect-ratio: 16/9;')

                # Chart panel
                with ui.card().classes('col-span-3 lg:col-span-1 card-bg shadow-lg p-6'):
                    ui.label('Bison Count Over Time').classes('text-lg font-medium text-gray-900 dark:text-white')
                    self.chart_count_label = ui.label(str(self.current_data["bison_count"])).classes('text-4xl font-bold primary-text')
                    
                    with ui.row().classes('items-center gap-2 mt-1'):
                        ui.label('Last 24 Hours').classes('text-sm text-gray-600 dark:text-gray-400')
                        ui.label('+5%').classes('text-sm font-medium text-green-500')
                    
                    # Chart
                    with ui.html().classes('chart-container mt-4'):
                        ui.html(self.chart_svg)
                    
                    # Time labels
                    with ui.row().classes('justify-between mt-2'):
                        for time_label in ['00:00', '06:00', '12:00', '18:00', '24:00']:
                            ui.label(time_label).classes('text-xs font-bold text-gray-500 dark:text-gray-400')

            # Real-time data cards
            ui.label('Real-Time Data').classes('text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4')
            
            with ui.grid(columns=6).classes('gap-4'):
                # Frame card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.frame_label = ui.label(str(self.current_data["frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
                # Bison count card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('Bison Count').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.count_label = ui.label(str(self.current_data["bison_count"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
                # FPS card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('FPS').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.fps_label = ui.label(str(self.current_data["fps"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
                # Total detections card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('Total Detections').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.total_label = ui.label(str(self.current_data["total_bison_detections"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
                # Max in frame card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('Max in Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.max_label = ui.label(str(self.current_data["max_bison_in_frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
                # Timestamp card
                with ui.card().classes('primary-bg p-4'):
                    ui.label('Timestamp').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                    self.timestamp_label = ui.label(self.format_timestamp(self.current_data["timestamp"])).classes('text-lg font-bold text-gray-900 dark:text-white')

    def run(self):
        """Run the application"""
        self.create_ui()
        # Start the data update loop
        ui.timer(2.0, self.update_data_sync)
        ui.run(title='Bison Tracker', dark=False, favicon='🦌')

    def update_data_sync(self):
        """Synchronous version of update_data for ui.timer"""
        # Simulate new data (replace with actual detection data)
        self.current_data.update({
            "frame": self.current_data["frame"] + random.randint(1, 5),
            "bison_count": random.randint(1, 25),
            "fps": random.randint(25, 35),
            "total_bison_detections": self.current_data["total_bison_detections"] + random.randint(0, 3),
            "max_bison_in_frame": max(self.current_data["max_bison_in_frame"], random.randint(1, 30)),
            "timestamp": time.time()
        })
        
        # Update UI elements
        self.update_ui_elements()

    def connect_to_detection_system(self, detection_callback):
        """
        Connect to your Python detection system
        Replace the simulated data with real detection data
        
        Args:
            detection_callback: Function that returns detection data in the format:
                {
                    "frame": int,
                    "bison_count": int,
                    "fps": float,
                    "total_bison_detections": int,
                    "max_bison_in_frame": int,
                    "timestamp": float
                }
        """
        def update_from_detection():
            new_data = detection_callback()
            if new_data:
                self.current_data.update(new_data)
                self.update_ui_elements()
        
        # Replace the timer with your detection system updates
        ui.timer(0.1, update_from_detection)  # Update more frequently for real-time


    

if __name__ in {"__main__", "__mp_main__"}:
    tracker =   BisonTracker()
    tracker.run()
# # Example usage
# if __name__ == "__main__":
#     tracker = BisonTracker()
#     tracker.run()
    
    # Example: Connect to your detection system
    # def get_detection_data():
    #     # Your detection logic here
    #     # Return data in the required format
    #     return {
    #         "frame": current_frame_number,
    #         "bison_count": detected_bison_count,
    #         "fps": current_fps,
    #         "total_bison_detections": total_count,
    #         "max_bison_in_frame": max_count,
    #         "timestamp": time.time()
    #     }
    # 
    # tracker.connect_to_detection_system(get_detection_data)
    
    
