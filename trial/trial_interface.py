import time
from datetime import datetime
import asyncio
import httpx
from nicegui import ui

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
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        ui.run_javascript(f'''
            document.documentElement.classList.toggle('dark', {str(self.is_dark_mode).lower()});
        ''')

    async def fetch_live_data(self):
        """Fetch live data from the detection server"""
        url = "http://127.0.0.1:8080/stats"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    for key in ["frame", "bison_count", "fps", "total_bison_detections", "max_bison_in_frame", "timestamp"]:
                        if key in data:
                            self.current_data[key] = data[key]
                    self.update_ui_elements()
                else:
                    print(f"Failed to fetch data: {response.status_code}")
            except Exception as e:
                print(f"Error fetching live data: {e}")

    async def update_data_live(self):
        """Continuously fetch live data every 2 seconds"""
        while True:
            await self.fetch_live_data()
            await asyncio.sleep(2)

    def update_ui_elements(self):
        """Update UI elements with current data"""
        self.chart_count_label.text = str(self.current_data["bison_count"])
        self.frame_label.text = str(self.current_data["frame"])
        self.count_label.text = str(self.current_data["bison_count"])
        self.fps_label.text = str(self.current_data["fps"])
        self.total_label.text = str(self.current_data["total_bison_detections"])
        self.max_label.text = str(self.current_data["max_bison_in_frame"])
        self.timestamp_label.text = self.format_timestamp(self.current_data["timestamp"])

    def create_ui(self):
        """Create the NiceGUI interface"""
        # Header
        with ui.header().classes('bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b'):
            with ui.row().classes('w-full items-center justify-between px-10 py-3'):
                ui.label('Bison Tracker').classes('text-xl font-bold')

        # Main content
        with ui.column().classes('px-8 py-6'):
            # Chart
            with ui.card().classes('p-4'):
                ui.label('Bison Count Over Time').classes('text-lg font-medium')
                self.chart_count_label = ui.label(str(self.current_data["bison_count"])).classes('text-4xl font-bold')
                ui.html(self.chart_svg).classes('mt-4')

            # Data cards
            with ui.grid(columns=6).classes('gap-4 mt-6'):
                for label, attr in [
                    ('Frame', 'frame'),
                    ('Bison Count', 'bison_count'),
                    ('FPS', 'fps'),
                    ('Total Detections', 'total_bison_detections'),
                    ('Max in Frame', 'max_bison_in_frame'),
                    ('Timestamp', 'timestamp')
                ]:
                    with ui.card().classes('p-4'):
                        ui.label(label)
                        value_label = ui.label(str(self.current_data[attr])).classes('text-2xl font-bold')
                        setattr(self, f"{attr}_label", value_label)

            # Dark mode toggle
            ui.button('Toggle Dark Mode', on_click=self.toggle_dark_mode).classes('mt-4')

    def run(self):
        """Run NiceGUI on port 8081 with async live update"""
        self.create_ui()
        # Schedule the async live data loop
        asyncio.get_event_loop().create_task(self.update_data_live())
        # Run NiceGUI frontend
        ui.run(title='Bison Tracker', dark=False, port=8081, favicon='🦌')


if __name__ in {"__main__", "__mp_main__"}:
    tracker = BisonTracker()
    tracker.run()


