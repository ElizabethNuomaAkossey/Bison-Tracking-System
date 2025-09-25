    self.create_ui()
        
        # Schedule the async live data loop in the current event loop
        loop = asyncio.get_event_loop()
        loop.create_task(self.update_data_live())
        
        # Run NiceGUI frontend
        ui.run(title='Bison Tracker', dark=False, port=8081, favicon='🦌')