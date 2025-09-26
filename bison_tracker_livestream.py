from nicegui import ui,app
import asyncio
import random
import time
from typing import Dict, Any
from datetime import datetime
import json
import cv2



# Exposing assets folder
app.add_static_files("/assets","assets")

@ui.page("/livestream")
def livestream():
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
        
            with ui.row().classes("w-full md:h-full md:gap-8 flex flex-wrap"):  # Main row
                # Left: Video
                with ui.card().classes("video-placeholder shadow-lg w-full lg:w-[60%] "):
                    ui.html(f'''
                        <div class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center ">
                            <div class="play-button">
                                <video src="Bison-tracked_new.mp4>
                                <svg width="48" height="48" fill="white" viewBox="0 0 24 24">
                                    <path d=video/>
                                </svg>
                            </div>
                        </div>
                    ''').style("position: relative; width: 100%; aspect-ratio: 16/9;")
                
                # Right: Stacked cards
                with ui.column().classes("w-full lg:w-[35%] gap-4"):  # Column for two cards
                    # Alerts card
                    with ui.card().classes(" w-full p-4 "):
                        ui.label("Alerts").classes("text-lg ")
                        # Add more content here (e.g., alert list or timestamps)
                    
                    # Bison Count Over Time card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("Bison Count Over Time").classes("text-lg")
                        # You can add the count or chart below the label
                        ui.label("15").classes("")  
                    # Bison movement card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("Bison Movement").classes('text-lg')

            with ui.element("div").classes('grid grid-cols-2 lg:grid-cols-6 gap-4 w-full'):
                # ui.label("Live Data").classes('text-2xl font-bold text-gray-900 dark:text-white')
                    # Frame card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.frame_label = ui.label(str(self.current_data["frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                    
                    # Bison count card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('Bison Count').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.count_label = ui.label(str(self.current_data["bison_count"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                    
                    # FPS card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('FPS').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.fps_label = ui.label(str(self.current_data["fps"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                    
                    # Total detections card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('Total Detections').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.total_label = ui.label(str(self.current_data["total_bison_detections"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                    
                    # Max in frame card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('Max in Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.max_label = ui.label(str(self.current_data["max_bison_in_frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                    
                    # Timestamp card
                with ui.card().classes('bg-green-200 p-4'):
                        ui.label('Timestamp').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
                        # self.timestamp_label = ui.label(self.format_timestamp(self.current_data["timestamp"])).classes('text-lg font-bold text-gray-900 dark:text-white')



        # # Video and Chart Grid
        # with ui.grid(columns=3).classes('w-full gap-8'):
        #     # Video player (spans 2 columns)
        #     with ui.column().classes('col-span-3 lg:col-span-2'):
        #         with ui.card().classes('video-placeholder shadow-lg'):
        #             ui.html('''
        #                 <div class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
        #                     <div class="play-button">
        #                         <svg width="48" height="48" fill="white" viewBox="0 0 24 24">
        #                             <path d="M8 5v14l11-7z"/>
        #                         </svg>
        #                     </div>
        #                 </div>
        #             ''').style('position: relative; width: 100%; aspect-ratio: 16/9;')

            #     # Chart panel
            #     with ui.card().classes('col-span-3 lg:col-span-1 card-bg shadow-lg p-6'):
            #         ui.label('Bison Count Over Time').classes('text-lg font-medium text-gray-900 dark:text-white')
            #         self.chart_count_label = ui.label(str(self.current_data["bison_count"])).classes('text-4xl font-bold primary-text')
                    
            #         with ui.row().classes('items-center gap-2 mt-1'):
            #             ui.label('Last 24 Hours').classes('text-sm text-gray-600 dark:text-gray-400')
            #             ui.label('+5%').classes('text-sm font-medium text-green-500')
                    
            #         # Chart
            #         with ui.html().classes('chart-container mt-4'):
            #             ui.html(self.chart_svg)
                    
            #         # Time labels
            #         with ui.row().classes('justify-between mt-2'):
            #             for time_label in ['00:00', '06:00', '12:00', '18:00', '24:00']:
            #                 ui.label(time_label).classes('text-xs font-bold text-gray-500 dark:text-gray-400')

            # # Real-time data cards
            # ui.label('Real-Time Data').classes('text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4')
            
            # with ui.grid(columns=6).classes('gap-4'):
            #     # Frame card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.frame_label = ui.label(str(self.current_data["frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
            #     # Bison count card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('Bison Count').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.count_label = ui.label(str(self.current_data["bison_count"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
            #     # FPS card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('FPS').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.fps_label = ui.label(str(self.current_data["fps"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
            #     # Total detections card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('Total Detections').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.total_label = ui.label(str(self.current_data["total_bison_detections"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
            #     # Max in frame card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('Max in Frame').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.max_label = ui.label(str(self.current_data["max_bison_in_frame"])).classes('text-2xl font-bold text-gray-900 dark:text-white')
                
            #     # Timestamp card
            #     with ui.card().classes('primary-bg p-4'):
            #         ui.label('Timestamp').classes('text-sm font-medium text-gray-600 dark:text-gray-300')
            #         self.timestamp_label = ui.label(self.format_timestamp(self.current_data["timestamp"])).classes('text-lg font-bold text-gray-900 dark:text-white')

                

