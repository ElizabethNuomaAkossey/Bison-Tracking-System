# 🦬 BisonGuard Dashboard

BisonGuard is a real-time monitoring system for detecting and tracking bison. It provides a **web dashboard** (powered by [NiceGUI](https://nicegui.io)) to visualize live statistics such as frame counts, bison detections, confidence scores, and movement trends.

---

## 📂 Project Structure

```
BisonGuard/
│
├── main.py                # Entry point (launches homepage + dashboard)
├── homepage.py            # Homepage UI
├── dashboard.py           # Dashboard UI (stats, charts, metrics)
├── bison_tracker_backend/ # (Optional) Backend services for detection
│   └── ... 
├── assets/                # Static assets (logo, images, css)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/BisonGuard.git
cd BisonGuard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate     # on macOS/Linux
venv\Scripts\activate        # on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, here are the core libraries:

```txt
nicegui
aiohttp
plotly
opencv-python
```

(You may add `requests`, `numpy`, or other libs if your backend uses them.)

---

## Running the Application

1. Start your backend (tracker/detector) — it should expose the `/stats` endpoint.  
   Example:
   ```
   http://localhost:8080/stats
   ```

   The `/stats` endpoint returns JSON like:

   ```json
   {
     "total_frames": 0,
     "total_detections": 0,
     "max_bison_in_frame": 0,
     "avg_confidence": 0.0,
     "fps": 0
   }
   ```

2. Run the app:
   ```bash
   python main.py
   ```

3. Open your browser at:
   ```
   http://localhost:5000
   ```

---

## 📡 API Endpoints

### Backend
- **`GET /stats`** → Returns live detection stats in JSON format:
  - `total_frames` → Number of frames processed  
  - `total_detections` → Total bison detected across frames  
  - `max_bison_in_frame` → Peak number of bison in a single frame  
  - `avg_confidence` → Average detection confidence  
  - `fps` → Frames per second  

### Frontend (NiceGUI app)
- **`/`** → Homepage (from `bison_tracker_homepage.py`)  
- **`/dashboard`** → Real-time dashboard (from `bison_tracker_dashboard.py`)  

---

## Architecture

1. **Backend (Detection Engine)**  
   - Runs the bison detection & tracking model.  
   - Publishes stats via `/stats` JSON endpoint.  

2. **Frontend (NiceGUI App)**  
   - `homepage.py` → Landing page for users.  
   - `dashboard.py` → Real-time stats, labels, and charts.  
   - `main.py` → Central entry point that imports homepage & dashboard, then starts the UI server.  

3. **Live Data Flow**
   ```
   Detection Backend → /stats → poll_stats() → Dashboard UI (Plotly + Cards)
   ```

---

## 📊 Dashboard Features

- **Metrics cards** showing:
  - Total Frames  
  - Total Detections  
  - Max Bison in Frame  
  - Average Confidence  
  - FPS  

- **Real-time chart** of bison movement (`max_bison_in_frame`) using Plotly.  
- **Automatic polling** of backend `/stats` every second.  

---

## Notes

- Ensure your backend server (with `/stats`) is running before launching the dashboard.  
- By default, the dashboard runs at `http://localhost:5000`. You can change the port in `ui.run(port=...)`.  
- Static assets (like logos) should go inside the `assets/` folder.  
