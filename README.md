<p align="center">
  <a href="https://ghosttrackerpro.vercel.app">
    <img src="https://img.shields.io/badge/GhostTrack_Pro-v3.1-00ff88?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e" alt="GhostTrack Pro">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Vercel-Deployed-000?logo=vercel&logoColor=white" alt="Vercel">
  <img src="https://img.shields.io/badge/License-Educational%20Only-yellow" alt="License">
  <img src="https://img.shields.io/github/stars/Hamza35779/GhostTrackerPro?style=social" alt="Stars">
</p>

<p align="center">
  <img src="images/Logo.jpg" alt="GhostTrack Pro Logo" width="120" style="border-radius: 16px;">
</p>

<p align="center">
  <img src="images/Banner.jpg" alt="GhostTrack Pro Banner" width="100%">
</p>

<h1 align="center">
  GhostTrack Pro
</h1>
<p align="center">
  <strong>Advanced OSINT & Educational Tracking Toolkit</strong>
  <br>
  <sub>IP Tracking · Phone Intelligence · Username OSINT · Live GPS Capture · Web Interface</sub>
</p>

<p align="center">
  <br>
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#web-interface">Web UI</a> •
  <a href="#deploy-to-vercel">Vercel</a> •
  <a href="#api-documentation">API</a> •
  <a href="#architecture">Architecture</a>
</p>

<p align="center">
  <sub>
    <strong>Live Demo:</strong>
    <a href="https://ghosttrackerpro.vercel.app">ghosttrackerpro.vercel.app</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>Repo:</strong>
    <a href="https://github.com/Hamza35779/GhostTrackerPro">github.com/Hamza35779/GhostTrackerPro</a>
  </sub>
</p>

---

**GhostTrack Pro** is a full-stack OSINT (Open Source Intelligence) reconnaissance and educational tracking platform designed for cybersecurity professionals, penetration testers, digital forensics researchers, and ethical hackers. It integrates five intelligence-gathering modules into a unified toolkit that can be operated via three distinct interfaces — terminal, local web browser, or globally deployed cloud instance.

### What It Does

GhostTrack Pro collects publicly available information from multiple sources to paint a picture of a target's digital footprint:

| Module | Data Collected | Source |
|---|---|---|
| **IP Address Intelligence** | Geolocation, ISP, organization, coordinates | ipwho.is API |
| **Phone Number Analysis** | Carrier, registered region, timezone, validity | Google libphonenumber |
| **Username OSINT** | Cross-platform social media presence | Direct HTTP checks (7 platforms) |
| **Live GPS Capture** | Real-time latitude/longitude, accuracy, IP | Browser Geolocation API via social engineering |
| **My IP** | Your own public IP, ISP, city, country | ipify.org + ipwho.is |

### Why Use It

- **All-in-one** — No need to juggle separate tools for IP, phone, username, and GPS tracking
- **Three interfaces** — Use the terminal, a local web UI, or deploy to the cloud
- **Auto-logging** — Every result is timestamped and saved to `logs/` automatically
- **Extensible architecture** — `core.py` contains all logic; adding new data sources is straightforward
- **Educational** — Demonstrates how easily location data can be phished and how much OSINT data is publicly available

### How to Interact

```
┌──────────────────────────────────────────────────────────────────┐
│                        GhostTrack Pro                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │  Terminal CLI        │  │  Local Web UI    │  │  Vercel     │ │
│  │  python3 app.py --ip │  │  :8080           │  │  .vercel.app│ │
│  │                      │  │                  │  │             │ │
│  │  • Interactive menu  │  │  • Dark theme    │  │  • Cloud    │ │
│  │  • CLI flags         │  │  • Card layout   │  │  • Public   │ │
│  │  • GPS server :5000  │  │  • REST API      │  │  • Serverless│ │
│  └─────────────────────┘  └──────────────────┘  └─────────────┘ │
│                                                                  │
│         All three share the same core.py backend                 │
└──────────────────────────────────────────────────────────────────┘
```

All three interfaces share the same backend logic in `core.py`, so results are identical regardless of how you run the tool. The CLI is best for quick lookups in the terminal, the local web UI provides a richer visual experience, and the Vercel deployment makes the toolkit accessible from any device with a browser.

---

## Disclaimer

> **This tool is for educational purposes and authorized testing only.**
> - Do **not** use this to track individuals without their explicit consent.
> - Unauthorized tracking may violate privacy laws (GDPR, CFAA, etc.) in your jurisdiction.
> - The developer is **not responsible** for any misuse of this tool.
> - The GPS capture feature works via a phishing-style link — use it **only** on your own devices or with written permission.

---

## Features

### 1. IP Address Intelligence
Retrieve public registration data for any IPv4 address via the [ipwho.is](https://ipwho.is) API.

| Field | Description |
|---|---|
| IP Address | The queried address |
| Type | IPv4 / IPv6 |
| Country | Registered country |
| City | Registered city |
| Region | State or region |
| ISP | Internet Service Provider |
| Organization | Owning organization |
| Coordinates | Approximate latitude/longitude |

**Limitation:** IP geolocation shows the ISP's registered location, not the user's physical address. It cannot identify a specific person or house.

---

### 2. Phone Number Intelligence
Analyze phone numbers for carrier, region, and validity using the [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) library (Google's libphonenumber).

| Field | Description |
|---|---|
| Country Code | International dialing code |
| National Number | Formatted local number |
| Registered Location | Geographic region of the carrier |
| Carrier / Operator | Mobile network operator |
| Timezone | Timezone(s) associated with the number |
| Valid Number | Whether the number format is valid |

**Limitation:** This provides carrier registration data only — not real-time GPS location. Real-time tracking requires the GPS capture module or legal interception.

---

### 3. Username OSINT
Check the existence of a username across major social media platforms.

| Platform | URL Pattern |
|---|---|
| Instagram | `https://instagram.com/{username}/` |
| Facebook | `https://facebook.com/{username}` |
| Twitter / X | `https://twitter.com/{username}` |
| GitHub | `https://github.com/{username}` |
| Reddit | `https://reddit.com/user/{username}` |
| TikTok | `https://tiktok.com/@{username}` |
| Pinterest | `https://pinterest.com/{username}/` |

Results are categorized as **Found**, **Not Found**, or **Blocked** (rate-limited / captcha). Some platforms may return false positives due to anti-bot measures.

---

### 4. Live GPS Tracker (Educational)

<p align="center">
  <img src="images/GPSTracker.jpeg" alt="GPS Tracker" width="60%">
</p>

Creates a local Flask web server that hosts a fake "Security Alert" page. When the target visits the link and clicks **"Verify & Secure Device"**, the browser's Geolocation API sends their coordinates to your terminal.

**Technical flow:**
1. Start the server on port 5000
2. Victim visits `http://your-ip:5000`
3. Page requests location permission
4. On acceptance, coordinates are sent to `/capture` endpoint
5. Data is printed to terminal and saved to `logs/`

**Requirements:** For remote targets, use a tunneling service (Ngrok, LocalXpose, Cloudflare Tunnel) to expose port 5000.

---

### 5. Web Interface (Browser UI)

A single-page web application with a dark theme, card-based navigation, and real-time API responses:

- IP Tracker — input form with results table
- Phone Tracker — carrier and location display
- Username Tracker — per-platform status badges
- My IP — one-click public IP lookup
- GPS Tracker — setup instructions
- Logs Browser — view all saved results

---

### 6. Auto-Save & Logging

Every result is automatically saved to `logs/` as a timestamped text file:

```
logs/
├── IP_TRACK_2026-07-05_14-30-22.txt
├── PHONE_TRACK_2026-07-05_14-31-05.txt
├── USERNAME_TRACK_2026-07-05_14-32-10.txt
└── GPS_CAPTURE_2026-07-05_14-33-00.txt
```

In CLI flag mode and web mode, saving is automatic. In interactive menu mode, you are prompted before saving.

---

## Installation

### Requirements

- **Python 3.8+**
- **pip** (Python package manager)
- **Operating System:** Linux (Kali, Ubuntu, Parrot), macOS, or Android (Termux)

### Linux (Kali / Ubuntu / Parrot)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git -y
git clone https://github.com/Hamza35779/GhostTrackerPro.git
cd GhostTrackerPro
pip3 install -r requirements.txt
python3 GhostTrackerPro.py
```

### macOS

```bash
# Install Python if needed: brew install python
git clone https://github.com/Hamza35779/GhostTrackerPro.git
cd GhostTrackerPro
pip3 install -r requirements.txt
python3 GhostTrackerPro.py
```

### Termux (Android)

> **Important:** Do not use the Play Store version of Termux — it is outdated. Download from [F-Droid](https://f-droid.org/en/packages/com.termux/) or the [official GitHub](https://github.com/termux/termux-app).

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/Hamza35779/GhostTrackerPro.git
cd GhostTrackerPro
pip install -r requirements.txt
python GhostTrackerPro.py
```

### Verify Installation

```bash
python3 GhostTrackerPro.py --myip
# Expected output: Your public IP address with ISP and location
```

---

## Usage

### Interactive Menu

```bash
python3 GhostTrackerPro.py
```

```
[ 1 ] IP Tracker (Info Only)
[ 2 ] Show Your IP
[ 3 ] Phone Number Tracker (Info Only)
[ 4 ] Username Tracker
[ 5 ] Live GPS Tracker
[ 6 ] Web Interface (Browser UI)
[ 0 ] Exit
```

### Command-Line Flags

```bash
# IP lookup (auto-saves result)
python3 GhostTrackerPro.py --ip 8.8.8.8

# Phone lookup
python3 GhostTrackerPro.py --phone +14155552671

# Username search
python3 GhostTrackerPro.py --username johndoe

# Your public IP
python3 GhostTrackerPro.py --myip

# GPS capture server
python3 GhostTrackerPro.py --gps

# Web interface
python3 GhostTrackerPro.py --web

# Help
python3 GhostTrackerPro.py --help
```

---

## Web Interface

Start the local web UI and open `http://localhost:8080` in your browser.

```bash
# From CLI menu
python3 GhostTrackerPro.py   # then select option 6

# From command line
python3 GhostTrackerPro.py --web

# Directly
python3 web/server.py
```

The web interface auto-detects your local network IP and displays it for sharing with other devices on your LAN.

---

## Deploy to Vercel

The web interface is live at:

<p align="center">
  <a href="https://ghosttrackerpro.vercel.app"><strong>https://ghosttrackerpro.vercel.app</strong></a>
</p>

### Deploy Your Own Instance

The project uses **zero-configuration Flask detection** — Vercel automatically detects `requirements.txt` and `app.py`.

**Option 1 — One-click:**
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Hamza35779/GhostTrackerPro)

**Option 2 — CLI:**
```bash
npm i -g vercel
git clone https://github.com/Hamza35779/GhostTrackerPro.git
cd GhostTrackerPro
vercel --prod
```

**Notes:**
- Logs use `/tmp/logs` (ephemeral — cleared between requests)
- GPS tracker (`--gps`) runs locally only — not on Vercel
- Python version: 3.12 (set via `.python-version`)

---

## API Documentation

The Flask backend exposes a REST API at `/api/*`. All endpoints return JSON.

### `GET /api/my-ip`

Returns your public IP and optional ISP/location data.

```bash
curl https://ghosttrackerpro.vercel.app/api/my-ip
```

```json
{
  "success": true,
  "data": {
    "ip": "20.192.21.48",
    "isp": "Microsoft Corporation",
    "country": "India",
    "city": "Pune"
  }
}
```

### `POST /api/ip-track`

Look up an IP address.

```bash
curl -X POST https://ghosttrackerpro.vercel.app/api/ip-track \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

```json
{
  "success": true,
  "data": {
    "ip": "8.8.8.8",
    "type": "IPv4",
    "country": "United States",
    "city": "Mountain View",
    "region": "California",
    "isp": "Google LLC",
    "organization": "Google LLC",
    "latitude": 37.3860517,
    "longitude": -122.0838511,
    "_saved": { "success": true, "path": "/tmp/logs/IP_TRACK_..." }
  }
}
```

### `POST /api/phone-track`

Analyze a phone number.

```bash
curl -X POST https://ghosttrackerpro.vercel.app/api/phone-track \
  -H "Content-Type: application/json" \
  -d '{"phone": "+14155552671"}'
```

```json
{
  "success": true,
  "data": {
    "phone": "+14155552671",
    "country_code": "+1",
    "national_number": "(415) 555-2671",
    "location": "San Francisco, CA",
    "carrier": "N/A",
    "timezone": "America/Los_Angeles",
    "is_valid": true,
    "_saved": { "success": true, "path": "/tmp/logs/PHONE_TRACK_..." }
  }
}
```

### `POST /api/username-track`

Search a username across social media.

```bash
curl -X POST https://ghosttrackerpro.vercel.app/api/username-track \
  -H "Content-Type: application/json" \
  -d '{"username": "github"}'
```

```json
{
  "success": true,
  "data": {
    "username": "github",
    "results": [
      { "platform": "Instagram", "url": "https://www.instagram.com/github/", "status": "found" },
      { "platform": "GitHub", "url": "https://github.com/github", "status": "found" },
      { "platform": "Facebook", "url": "https://www.facebook.com/github", "status": "blocked", "code": 400 }
    ],
    "_saved": { "success": true, "path": "/tmp/logs/USERNAME_TRACK_..." }
  }
}
```

### `GET /api/logs`

Retrieve up to 50 most recent saved log entries.

```bash
curl https://ghosttrackerpro.vercel.app/api/logs
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   GhostTrack Pro                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐    ┌───────────┐    ┌──────────────┐  │
│  │ CLI      │    │ Flask Web │    │ Vercel (Cloud)│  │
│  │ Termux / │───▶│ Server    │───▶│ Serverless    │  │
│  │ Linux    │    │ Port 8080 │    │ Function      │  │
│  └──────────┘    └───────────┘    └──────────────┘  │
│        │               │               │             │
│        ▼               ▼               ▼             │
│  ┌─────────────────────────────────────────────────┐│
│  │              core.py (Shared Logic)              ││
│  │  track_ip · track_phone · track_username         ││
│  │  get_my_ip · get_local_ip · save_result · read   ││
│  └─────────────────────────────────────────────────┘│
│        │                                             │
│        ▼                                             │
│  ┌─────────────────────────────────────────────────┐│
│  │  External APIs & Libraries                       ││
│  │  ipwho.is · ipify.org · phonenumbers · requests ││
│  └─────────────────────────────────────────────────┘│
│                                                      │
└─────────────────────────────────────────────────────┘
```

All three interfaces (CLI, local web, Vercel web) import the same functions from `core.py`. Results are identical regardless of the interface used.

---

## File Structure

```
GhostTrackPro/
│
├── app.py                   # Flask app (Vercel auto-detects this)
├── core.py                  # Shared logic layer (data functions)
├── GhostTrackerPro.py       # CLI entry point with argparse
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment config
├── .python-version          # Python version pin (3.12)
├── .gitignore
├── .vercelignore
├── README.md
│
├── images/
│   ├── Home.png             # Screenshot of the main interface
│   └── GPSTracker.jpeg      # Screenshot of the GPS tracker
│
├── logs/                    # Auto-created; stores all results
│
├── web/
│   ├── __init__.py
│   ├── server.py            # Imports app from app.py (local dev)
│   ├── static/
│   │   └── style.css        # Dark-theme responsive CSS
│   └── templates/
│       └── index.html       # Single-page application
│
└── .vercel/                 # Created by `vercel` CLI (gitignored)
    ├── project.json
    └── README.txt
```

---

## FAQ

**Q: Can I track a phone's real-time location just by entering the number?**  
**A:** No. Real-time GPS requires the Live GPS Tracker feature, which needs the target to click a link and grant browser location permission. Phone number lookup only provides carrier registration data.

**Q: Can I find someone's exact address from their IP?**  
**A:** No. IP geolocation returns the ISP's registered city/region — not a street address or specific person.

**Q: Why does the GPS tracker need Flask?**  
**A:** The GPS tracker runs a local Flask web server on port 5000 to serve the phishing page and receive the Geolocation API callback.

**Q: Is this legal?**  
**A:** The tool is legal for educational purposes and authorized testing (your own devices or with written consent). Using it to track someone without permission may violate local privacy laws.

**Q: Can I use this on Termux?**  
**A:** Yes. Install Python, clone the repo, run `pip install -r requirements.txt`, then `python GhostTrackerPro.py`.

**Q: Why does the Vercel deploy show no logs?**  
**A:** Vercel's filesystem is read-only except for `/tmp`. Logs are written to `/tmp/logs` but are ephemeral — they don't persist between requests.

---

## License

This project is licensed for **educational use only**. By using this tool, you agree to comply with all applicable local and international laws regarding privacy, data protection, and computer misuse.

**Version:** 3.1 · Web Edition
