# GhostTrack Pro

![Home](images/Home.jpeg)

**GhostTrack Pro** is an advanced OSINT (Open Source Intelligence) and educational tracking tool designed for cybersecurity professionals, researchers, and ethical hackers. It combines traditional information gathering with a real-time GPS phishing module to demonstrate how location data can be captured via social engineering.

> **DISCLAIMER:** This tool is for **educational purposes and authorized testing only**.
> - Do not use this to track individuals without their explicit consent.
> - Unauthorized tracking may violate privacy laws and computer misuse acts in your jurisdiction.
> - The developer is not responsible for misuse of this tool.

## Capabilities

### 1. IP Information Gathering
- Retrieves public registration data for any IP address.
- **Data Provided:** Country, City, ISP, Organization, Region, Coordinates.
- **Limitation:** Provides registration info, **not** real-time GPS location.

### 2. Phone Number Intelligence
- Analyzes phone numbers for validity and carrier information.
- **Data Provided:** Carrier name, registered region/country, timezone, validity status.
- **Limitation:** Cannot track real-time GPS location of a phone number without a warrant or spyware.

### 3. Username OSINT
- Checks the existence of a username across major social media platforms (Facebook, Instagram, Twitter/X, GitHub, Reddit, TikTok, Pinterest).
- Helps identify a target's digital footprint.

### 4. Live GPS Tracker
![GPS Tracker](images/GPSTracker.jpeg)
- **How it works:** Creates a local web server that generates a "trap" link (e.g., a fake security alert page).
- **The Attack:** When the target clicks the link and grants location permission, their **exact real-time GPS coordinates** and IP address are sent to your terminal.
- **Use Case:** Demonstrates the dangers of granting location permissions to unknown links.
- **Requirement:** For remote targets (outside your WiFi), this feature requires a tunneling service like **Ngrok** or **Localxpose** to expose your local server to the internet.

### 5. Web Interface (Browser UI)
- A modern, responsive web UI for all tracking features.
- Accessible from any browser on your local network.
- Can be deployed to Vercel for global access.
- Results displayed in a clean card layout with auto-save to logs.

## Requirements
- **Python 3.8+** (Required)
- **Operating System:** Linux (Kali, Ubuntu, etc.), macOS, or Android (Termux).
- **Dependencies:**
  - `requests` (For API calls)
  - `phonenumbers` (For phone analysis)
  - `flask` (For the web server and GPS tracker)

## Installation & Setup

### Linux (Kali / Parrot OS / Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git -y
git clone https://github.com/akramlatif/GhostTrackerPro.git
cd GhostTrackerPro
pip3 install -r requirements.txt
python3 GhostTrackerPro.py
```

### Termux (Android)

> **Note:** Do not use the Play Store version of Termux. Download it from F-Droid or the official GitHub repository.

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/akramlatif/GhostTrackerPro.git
cd GhostTrackerPro
pip install -r requirements.txt
python GhostTrackerPro.py
```

### macOS

```bash
# Install Python if you don't have it: brew install python
git clone https://github.com/akramlatif/GhostTrackerPro.git
cd GhostTrackerPro
pip3 install -r requirements.txt
python3 GhostTrackerPro.py
```

## Usage

### Interactive Menu Mode

```bash
python3 GhostTrackerPro.py
```

Select an option by entering its number:
- `1` - IP Tracker
- `2` - Show Your IP
- `3` - Phone Number Tracker
- `4` - Username Tracker
- `5` - Live GPS Tracker
- `6` - Web Interface (Browser UI)
- `0` - Exit

### Command-Line Mode

```bash
python3 GhostTrackerPro.py --ip 8.8.8.8
python3 GhostTrackerPro.py --phone +14155552671
python3 GhostTrackerPro.py --username johndoe
python3 GhostTrackerPro.py --myip
python3 GhostTrackerPro.py --gps
python3 GhostTrackerPro.py --web
python3 GhostTrackerPro.py --help
```

### Web Interface

The web interface provides a modern browser-based UI for all tracking features. Start it in two ways:

**From the CLI menu:** Select option `6` (Web Interface)

**From the command line:**
```bash
python3 GhostTrackerPro.py --web
```

**Directly:**
```bash
python3 web/server.py
```

Then open your browser to:
- **Local:** http://localhost:8080
- **Network:** http://YOUR_IP:8080 (accessible from other devices on your network)

The web interface includes:
- Dashboard with clickable cards for each tool
- Form inputs with Enter-key support
- Real-time results displayed in styled cards
- Auto-save of all results to the logs directory
- Logs browser to view past results
- Dark theme optimized for long use

### Auto-Save Results

Results are automatically saved to the `logs/` directory. In CLI mode you'll be prompted to save; in CLI flag mode and web mode, saving is automatic.

```
logs/
├── IP_TRACK_2026-07-05_14-30-22.txt
├── PHONE_TRACK_2026-07-05_14-31-05.txt
└── USERNAME_TRACK_2026-07-05_14-32-10.txt
```

### How to Use the Live GPS Tracker

The Live GPS Tracker works in two scenarios:

#### Scenario 1: Local Network (Same WiFi)
- Run the GPS tracker (option 5 or `--gps`).
- Send the `http://192.168.x.x:5000` link to the target on the same network.
- If they click and allow location, you will see their coordinates.

#### Scenario 2: Remote Network (Internet)
Use a tunneling service like Ngrok to expose your local server:

```bash
ngrok http 5000
```

Use the generated `https://...` link instead of the local IP.

## FAQ & Limitations

**Q:** Can I track a phone's real-time location just by entering the number?
**A:** No. This tool provides carrier/registration info only. Real-time GPS requires the Live GPS Tracker feature, which needs the target to click a link and grant permission.

**Q:** Can I track someone's IP to their exact house?
**A:** No. IP addresses only reveal the ISP's server location (City/Region).

**Q:** Why do I need Flask?
**A:** Flask powers both the web interface and the Live GPS Tracker server.

**Q:** Is this legal?
**A:** Yes, for educational purposes and authorized testing. Using it without consent may be illegal.

## Deploy to Vercel

You can deploy the web interface to Vercel for free, making it accessible from anywhere.

### Prerequisites

- A [Vercel](https://vercel.com) account (free tier works)
- [Vercel CLI](https://vercel.com/docs/cli) installed: `npm i -g vercel`

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/akramlatif/GhostTrackerPro)

### Manual Deploy

```bash
# Clone the repo
git clone https://github.com/akramlatif/GhostTrackerPro.git
cd GhostTrackerPro

# Deploy to Vercel
vercel
```

Follow the CLI prompts. The app will be available at `https://your-project.vercel.app`.

### Vercel Notes

- The `api/index.py` file is the Vercel entry point — it imports the Flask app from `web/server.py`.
- On Vercel, the logs directory uses `/tmp/logs` (ephemeral). Logs persist only during the request.
- The GPS tracker feature (`--gps`) cannot run on Vercel — it requires a local machine to bind to port 5000.
- The CLI mode (`--ip`, `--phone`, etc.) runs in your terminal and is unaffected by Vercel deployment.

## File Structure

```
GhostTrackPro/
├── api/
│   └── index.py            # Vercel serverless entry point
├── GhostTrackerPro.py      # CLI main script
├── core.py                 # Shared logic (used by CLI + web)
├── requirements.txt        # Dependencies
├── vercel.json             # Vercel deployment config
├── .vercelignore           # Files to exclude from deploy
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── images/                 # Screenshots
│   ├── Home.jpeg
│   └── GPSTracker.jpeg
├── logs/                   # (Auto-created) Stores captured data
└── web/                    # Web interface
    ├── __init__.py
    ├── server.py           # Flask app with API + frontend
    ├── static/
    │   └── style.css       # Dark-themed responsive styles
    └── templates/
        └── index.html      # Single-page web interface
```

## Architecture

The project uses a clean layered architecture:

- **`core.py`** - Pure logic functions that return data dictionaries. No I/O, no terminal interaction.
- **`GhostTrackerPro.py`** - CLI interface that imports `core.py` and handles terminal I/O (input/print).
- **`web/server.py`** - Flask web server that imports `core.py` and exposes REST API endpoints, serving the frontend.

This means both the CLI and web interface share the exact same tracking logic, ensuring consistent results.

## License

This project is licensed for educational use only. By using this tool, you agree to comply with all local and international laws regarding privacy and data protection.

**Version:** 3.0 (Web Edition)
