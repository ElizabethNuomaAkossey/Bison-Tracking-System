# BisonTracker

BisonTracker is a **real-time monitoring dashboard** for tracking bison activity. It fetches live detection data from a server and displays metrics such as frame count, bison count, FPS, total detections, maximum bison in a frame, and timestamp. The frontend is built using **NiceGUI** and updates dynamically every 2 seconds.

---

## Features

- Live data fetching from a remote server.
- Real-time dashboard displaying:
  - Current frame
  - Bison count
  - FPS (Frames Per Second)
  - Total bison detections
  - Maximum bison in a frame
  - Last updated timestamp
- Interactive dark mode toggle.
- Bison count trend chart.

---

## Requirements

- Python 3.10+
- [NiceGUI](https://nicegui.io/)
- [httpx](https://www.python-httpx.org/) for async HTTP requests

Install dependencies using pip:

```bash
pip install nicegui httpx


## Setup Instructions
- git clone https://github.com/yourusername/BisonTracker.git
- cd main.py

## 
# Default URL in BisonTracker.py
- LIVE_SERVER_URL = "http://127.0.0.1:8080/stats"

##Adjust frontend port 
- ui.run(title='Bison Tracker', dark=False, port=8081, favicon='🦌')

## Running the Application

To start the BisonTracker dashboard, simply run the `main.py` file:
