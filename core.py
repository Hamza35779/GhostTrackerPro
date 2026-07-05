import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import socket
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('VERCEL'):
    LOGS_DIR = '/tmp/logs'
else:
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

PLATFORMS = {
    "Instagram": "https://www.instagram.com/{username}/",
    "Facebook": "https://www.facebook.com/{username}",
    "Twitter/X": "https://twitter.com/{username}",
    "GitHub": "https://github.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "Pinterest": "https://www.pinterest.com/{username}/"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def ensure_logs_dir():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)


def save_result(data_type, data):
    ensure_logs_dir()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{data_type}_{timestamp}.txt"
    filepath = os.path.join(LOGS_DIR, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(f"{data_type} Result:\n")
            f.write("-" * 50 + "\n")
            f.write(data + "\n")
            f.write("-" * 50 + "\n")
        return {"success": True, "path": filepath}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def track_ip(ip):
    req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
    req_api.raise_for_status()
    ip_data = json.loads(req_api.text)
    return {
        "ip": ip,
        "type": ip_data.get("type", "N/A"),
        "country": ip_data.get("country", "N/A"),
        "city": ip_data.get("city", "N/A"),
        "region": ip_data.get("region", "N/A"),
        "isp": ip_data.get("connection", {}).get("isp", "N/A"),
        "organization": ip_data.get("connection", {}).get("org", "N/A"),
        "latitude": ip_data.get("latitude", "N/A"),
        "longitude": ip_data.get("longitude", "N/A"),
    }


def get_my_ip():
    resp = requests.get('https://api.ipify.org/', timeout=10)
    resp.raise_for_status()
    ip = resp.text
    result = {"ip": ip}
    try:
        extra = track_ip(ip)
        result["isp"] = extra["isp"]
        result["country"] = extra["country"]
        result["city"] = extra["city"]
    except Exception:
        pass
    return result


def track_phone(phone):
    if not phone.startswith('+'):
        phone = '+' + phone
    parsed = phonenumbers.parse(phone, None)
    location = geocoder.description_for_number(parsed, "en")
    provider = carrier.name_for_number(parsed, "en")
    zones = timezone.time_zones_for_number(parsed)
    valid = phonenumbers.is_valid_number(parsed)
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    return {
        "phone": phone,
        "country_code": f"+{parsed.country_code}",
        "national_number": national,
        "location": location or "N/A",
        "carrier": provider or "N/A",
        "timezone": ', '.join(zones) if zones else "N/A",
        "is_valid": valid,
    }


def track_username(username):
    results = []
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                results.append({"platform": platform, "url": url, "status": "found"})
            elif resp.status_code == 404:
                results.append({"platform": platform, "url": url, "status": "not_found"})
            else:
                results.append({"platform": platform, "url": url, "status": "blocked", "code": resp.status_code})
        except requests.exceptions.RequestException:
            results.append({"platform": platform, "url": url, "status": "error"})
    return {"username": username, "results": results}


def read_logs():
    ensure_logs_dir()
    files = sorted(os.listdir(LOGS_DIR), reverse=True)[:50]
    entries = []
    for f in files:
        if f.endswith('.txt'):
            path = os.path.join(LOGS_DIR, f)
            try:
                with open(path, 'r') as fh:
                    content = fh.read()
                entries.append({"filename": f, "path": path, "content": content[:500]})
            except Exception:
                entries.append({"filename": f, "path": path, "content": "(unreadable)"})
    return entries
