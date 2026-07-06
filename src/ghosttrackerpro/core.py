import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import socket
import ssl
from datetime import datetime
import os
import re
import subprocess
import concurrent.futures
from urllib.parse import urlparse

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('VERCEL'):
    LOGS_DIR = '/tmp/logs'
else:
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
TIMEOUT = 15

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    993, 995, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 6379,
    8080, 8443, 9000, 27017
]

PLATFORMS = {
    "Instagram": "https://www.instagram.com/{username}/",
    "Facebook": "https://www.facebook.com/{username}",
    "Twitter/X": "https://twitter.com/{username}",
    "GitHub": "https://github.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "Pinterest": "https://www.pinterest.com/{username}/",
    "LinkedIn": "https://www.linkedin.com/in/{username}/",
    "YouTube": "https://www.youtube.com/@{username}",
    "Snapchat": "https://www.snapchat.com/add/{username}",
    "Telegram": "https://t.me/{username}",
    "Twitch": "https://www.twitch.tv/{username}",
    "Medium": "https://medium.com/@{username}",
    "Steam": "https://steamcommunity.com/id/{username}",
    "DeviantArt": "https://www.deviantart.com/{username}",
    "Behance": "https://www.behance.net/{username}",
    "Keybase": "https://keybase.io/{username}",
    "Mastodon": "https://mastodon.social/@{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Spotify": "https://open.spotify.com/user/{username}",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 1. IP Tracking
# ---------------------------------------------------------------------------

def track_ip(ip):
    req_api = requests.get(f"http://ipwho.is/{ip}", timeout=TIMEOUT)
    req_api.raise_for_status()
    ip_data = json.loads(req_api.text)
    return {
        "ip": ip,
        "type": ip_data.get("type", "N/A"),
        "country": ip_data.get("country", "N/A"),
        "country_code": ip_data.get("country_code", "N/A"),
        "city": ip_data.get("city", "N/A"),
        "region": ip_data.get("region", "N/A"),
        "isp": ip_data.get("connection", {}).get("isp", "N/A"),
        "organization": ip_data.get("connection", {}).get("org", "N/A"),
        "latitude": ip_data.get("latitude", "N/A"),
        "longitude": ip_data.get("longitude", "N/A"),
        "flag": ip_data.get("flag", {}).get("emoji", ""),
    }


def get_my_ip():
    resp = requests.get('https://api.ipify.org/', timeout=TIMEOUT)
    resp.raise_for_status()
    ip = resp.text
    result = {"ip": ip}
    try:
        extra = track_ip(ip)
        result["isp"] = extra["isp"]
        result["country"] = extra["country"]
        result["city"] = extra["city"]
        result["flag"] = extra["flag"]
    except Exception:
        pass
    return result


# ---------------------------------------------------------------------------
# 2. Phone Tracking
# ---------------------------------------------------------------------------

def track_phone(phone):
    if not phone.startswith('+'):
        phone = '+' + phone
    parsed = phonenumbers.parse(phone, None)
    location = geocoder.description_for_number(parsed, "en")
    provider = carrier.name_for_number(parsed, "en")
    zones = timezone.time_zones_for_number(parsed)
    valid = phonenumbers.is_valid_number(parsed)
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return {
        "phone": phone,
        "country_code": f"+{parsed.country_code}",
        "national_number": national,
        "international": intl,
        "location": location or "N/A",
        "carrier": provider or "N/A",
        "timezone": ', '.join(zones) if zones else "N/A",
        "is_valid": valid,
        "country": phonenumbers.region_code_for_number(parsed) or "N/A",
    }


# ---------------------------------------------------------------------------
# 3. Username Tracking
# ---------------------------------------------------------------------------

def track_username(username):
    results = []
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200:
                results.append({"platform": platform, "url": url, "status": "found"})
            elif resp.status_code == 404:
                results.append({"platform": platform, "url": url, "status": "not_found"})
            elif resp.status_code == 429:
                results.append({"platform": platform, "url": url, "status": "rate_limited"})
            else:
                results.append({"platform": platform, "url": url, "status": "blocked", "code": resp.status_code})
        except requests.exceptions.Timeout:
            results.append({"platform": platform, "url": url, "status": "timeout"})
        except requests.exceptions.RequestException:
            results.append({"platform": platform, "url": url, "status": "error"})
    return {"username": username, "results": results, "total": len(results), "found": sum(1 for r in results if r['status'] == 'found')}


# ---------------------------------------------------------------------------
# 4. Subdomain Enumeration (via crt.sh)
# ---------------------------------------------------------------------------

def enumerate_subdomains(domain):
    domain = domain.strip().lower()
    if not domain:
        return {"domain": domain, "subdomains": [], "count": 0, "error": "No domain provided"}
    try:
        resp = requests.get(
            f"https://crt.sh/?q=%25.{domain}&output=json",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        resp.raise_for_status()
        entries = resp.json()
        subdomains = set()
        for entry in entries:
            name = entry.get("name_value", "")
            for n in name.split("\n"):
                n = n.strip().lower()
                if n.endswith(f".{domain}") or n == domain:
                    if n != domain:
                        subdomains.add(n)
        sorted_subs = sorted(subdomains)
        return {"domain": domain, "subdomains": sorted_subs, "count": len(sorted_subs), "error": None}
    except requests.exceptions.Timeout:
        return {"domain": domain, "subdomains": [], "count": 0, "error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"domain": domain, "subdomains": [], "count": 0, "error": str(e)}
    except (json.JSONDecodeError, ValueError) as e:
        return {"domain": domain, "subdomains": [], "count": 0, "error": f"Parse error: {e}"}


# ---------------------------------------------------------------------------
# 5. DNS Lookup
# ---------------------------------------------------------------------------

def dns_lookup(domain):
    domain = domain.strip().lower()
    records = {}
    try:
        records["A"] = [addr[4][0] for addr in socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)]
    except Exception:
        records["A"] = []

    try:
        records["AAAA"] = [addr[4][0] for addr in socket.getaddrinfo(domain, 80, socket.AF_INET6, socket.SOCK_STREAM)]
    except Exception:
        records["AAAA"] = []

    try:
        result = subprocess.run(
            ["nslookup", "-type=MX", domain],
            capture_output=True, text=True, timeout=5
        )
        mx_lines = [l for l in result.stdout.split("\n") if "mail exchanger" in l.lower()]
        mx_records = []
        for line in mx_lines:
            parts = line.split("=")
            if len(parts) > 1:
                mx_records.append(parts[-1].strip())
        records["MX"] = mx_records
    except Exception:
        records["MX"] = []

    try:
        result = subprocess.run(
            ["nslookup", "-type=NS", domain],
            capture_output=True, text=True, timeout=5
        )
        ns_lines = [l for l in result.stdout.split("\n") if "nameserver" in l.lower() and "=" in l]
        ns_records = []
        for line in ns_lines:
            parts = line.split("=")
            if len(parts) > 1:
                ns_records.append(parts[-1].strip().rstrip("."))
        records["NS"] = ns_records
    except Exception:
        records["NS"] = []

    try:
        result = subprocess.run(
            ["nslookup", "-type=TXT", domain],
            capture_output=True, text=True, timeout=5
        )
        txt_lines = [l for l in result.stdout.split("\n") if "text =" in l.lower() or '"' in l]
        records["TXT"] = [l.strip() for l in txt_lines[:10]]
    except Exception:
        records["TXT"] = []

    try:
        result = subprocess.run(
            ["nslookup", "-type=CNAME", domain],
            capture_output=True, text=True, timeout=5
        )
        cname_lines = [l for l in result.stdout.split("\n") if "canonical name" in l.lower() or "cname" in l.lower()]
        records["CNAME"] = [l.strip() for l in cname_lines]
    except Exception:
        records["CNAME"] = []

    try:
        result = subprocess.run(
            ["nslookup", "-type=SOA", domain],
            capture_output=True, text=True, timeout=5
        )
        soa_lines = [l for l in result.stdout.split("\n") if "primary name server" in l.lower() or "origin" in l.lower() or "soa" in l.lower()]
        records["SOA"] = [l.strip() for l in soa_lines]
    except Exception:
        records["SOA"] = []

    return {"domain": domain, "records": records}


# ---------------------------------------------------------------------------
# 6. Email Breach Check (Have I Been Pwned API - k-anonymity)
# ---------------------------------------------------------------------------

def email_breach_check(email):
    email = email.strip().lower()
    result = {"email": email, "breaches": [], "pastes": [], "error": None}
    if not email or "@" not in email:
        result["error"] = "Invalid email address"
        return result
    try:
        import hashlib
        sha1_hash = hashlib.sha1(email.encode()).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        resp.raise_for_status()
        for line in resp.text.split("\n"):
            if line.strip():
                line_suffix, count = line.strip().split(":")
                if line_suffix.upper() == suffix.upper():
                    result["breaches"].append({"source": "Have I Been Pwned", "hash_suffix": suffix, "count": int(count)})
        result["compromised"] = len(result["breaches"]) > 0
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
    return result


# ---------------------------------------------------------------------------
# 7. Hash Lookup (via public APIs)
# ---------------------------------------------------------------------------

def hash_lookup(hash_value):
    hash_value = hash_value.strip().lower()
    result = {"hash": hash_value, "found": False, "plaintext": None, "type": None, "error": None}
    if len(hash_value) == 32:
        result["type"] = "MD5"
    elif len(hash_value) == 40:
        result["type"] = "SHA1"
    elif len(hash_value) == 64:
        result["type"] = "SHA256"
    else:
        result["error"] = "Unrecognized hash length. Supported: MD5 (32), SHA1 (40), SHA256 (64)"
        return result

    try:
        resp = requests.get(
            f"https://www.nitrxgen.io/api/v1/check/{hash_value}",
            headers={"x-api-key": ""},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("plaintext"):
                result["found"] = True
                result["plaintext"] = data["plaintext"]
                return result
    except Exception:
        pass

    try:
        resp = requests.get(
            f"https://md5decrypt.net/Api/api.php?hash={hash_value}&hash_type={result['type'].lower()}&email=test@test.com&code=test",
            timeout=5
        )
        if resp.status_code == 200 and resp.text and "error" not in resp.text.lower() and resp.text.strip() != hash_value:
            result["found"] = True
            result["plaintext"] = resp.text.strip()
            return result
    except Exception:
        pass

    return result


# ---------------------------------------------------------------------------
# 8. Port Scanner
# ---------------------------------------------------------------------------

def _scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            service = socket.getservbyport(port, 'tcp') if port in [21,22,23,25,53,80,110,143,443,993,995,3306,3389,5432,5900,6379,8080,8443] else ""
            return {"port": port, "state": "open", "service": service}
        return None
    except Exception:
        return None


def port_scan(host, ports=None):
    if ports is None:
        ports = COMMON_PORTS
    open_ports = []
    errors = []
    try:
        socket.getaddrinfo(host, 80)
    except socket.gaierror:
        return {"host": host, "open_ports": [], "error": "Could not resolve hostname"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        fut_map = {executor.submit(_scan_port, host, p): p for p in ports}
        for fut in concurrent.futures.as_completed(fut_map):
            try:
                result = fut.result()
                if result:
                    open_ports.append(result)
            except Exception as e:
                errors.append(str(e))

    open_ports.sort(key=lambda x: x["port"])
    return {"host": host, "open_ports": open_ports, "total_open": len(open_ports), "ports_scanned": len(ports), "error": None}


# ---------------------------------------------------------------------------
# 9. WHOIS Lookup (via RDAP)
# ---------------------------------------------------------------------------

def whois_lookup(domain):
    domain = domain.strip().lower()
    result = {"domain": domain, "data": {}, "error": None}
    try:
        tld = domain.split(".")[-1]
        resp = requests.get(
            f"https://rdap.verisign.com/{tld}/v1/domain/{domain}",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if resp.status_code == 200:
            data = resp.json()
            events = {e["eventAction"]: e["eventDate"] for e in data.get("events", [])}
            entities = data.get("entities", [])
            registrant = ""
            for ent in entities:
                vcards = ent.get("vcardArray", [])
                if len(vcards) > 1:
                    for item in vcards[1]:
                        if item[0] == "fn":
                            registrant = item[3]
            nameservers = [ns["ldhName"] for ns in data.get("nameservers", [])]
            result["data"] = {
                "domain": data.get("ldhName", domain),
                "registrant": registrant or "N/A",
                "creation_date": events.get("registration", "N/A"),
                "expiration_date": events.get("expiration", "N/A"),
                "last_changed": events.get("last changed", "N/A"),
                "nameservers": nameservers,
                "dnssec": data.get("secureDNS", {}).get("delegationSigned", False),
            }
        else:
            result["error"] = f"RDAP returned {resp.status_code}"
    except requests.exceptions.Timeout:
        result["error"] = "Request timed out"
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    return result


# ---------------------------------------------------------------------------
# 10. URL / Header Analysis
# ---------------------------------------------------------------------------

def analyze_url(target_url):
    result = {
        "url": target_url,
        "final_url": None,
        "status_code": None,
        "headers": {},
        "security_headers": {},
        "redirect_chain": [],
        "server": None,
        "content_type": None,
        "error": None,
    }
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url
    try:
        resp = requests.get(target_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        result["final_url"] = resp.url
        result["status_code"] = resp.status_code
        result["server"] = resp.headers.get("Server", "N/A")
        result["content_type"] = resp.headers.get("Content-Type", "N/A")
        result["headers"] = dict(resp.headers)

        sec_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "Permissions-Policy",
            "X-Powered-By",
        ]
        for h in sec_headers:
            val = resp.headers.get(h)
            if val:
                result["security_headers"][h] = val

        for resp_h in resp.history:
            result["redirect_chain"].append({"url": resp_h.url, "status": resp_h.status_code})

        result["redirect_count"] = len(resp.history)
        result["parsed"] = {
            "scheme": urlparse(resp.url).scheme,
            "hostname": urlparse(resp.url).hostname,
            "path": urlparse(resp.url).path,
        }
    except requests.exceptions.Timeout:
        result["error"] = "Connection timed out"
    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL Error: {e}"
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection failed: {e}"
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
    return result


# ---------------------------------------------------------------------------
# 11. SSL Certificate Check
# ---------------------------------------------------------------------------

def ssl_check(hostname, port=443):
    hostname = hostname.strip().lower()
    result = {
        "hostname": hostname,
        "port": port,
        "valid": False,
        "issuer": None,
        "subject": None,
        "expiry": None,
        "issued": None,
        "serial": None,
        "fingerprint": None,
        "error": None,
    }
    try:
        if hostname.startswith("https://"):
            hostname = hostname.split("//")[1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                result["valid"] = True
                result["subject"] = dict(cert.get("subject", []))
                result["issuer"] = dict(cert.get("issuer", []))
                result["expiry"] = cert.get("notAfter", "N/A")
                result["issued"] = cert.get("notBefore", "N/A")
                result["serial"] = hex(ssock.server_certificate.get("serialNumber", 0)) if hasattr(ssock, 'server_certificate') else "N/A"
                result["version"] = cert.get("version", "N/A")
                result["sni"] = hostname
    except ssl.SSLCertVerificationError as e:
        result["error"] = f"SSL cert verification failed: {e}"
        result["valid"] = False
    except socket.timeout:
        result["error"] = "Connection timed out"
    except socket.gaierror:
        result["error"] = "Could not resolve hostname"
    except ConnectionRefusedError:
        result["error"] = "Connection refused"
    except Exception as e:
        result["error"] = str(e)
    return result


# ---------------------------------------------------------------------------
# 12. IP Reputation / Threat Check
# ---------------------------------------------------------------------------

def ip_reputation(ip):
    result = {"ip": ip, "reports": [], "is_vpn": False, "is_proxy": False, "is_tor": False, "abuse_score": 0, "error": None}
    try:
        resp = requests.get(f"http://ipwho.is/{ip}", timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        security = data.get("security", {})
        result["is_vpn"] = security.get("vpn", False)
        result["is_proxy"] = security.get("proxy", False)
        result["is_tor"] = security.get("tor", False)
        result["threat"] = security.get("threat_level", "unknown")
    except Exception as e:
        result["error"] = str(e)
    return result


# ---------------------------------------------------------------------------
# 13. Bulk Lookup
# ---------------------------------------------------------------------------

def bulk_ip_lookup(ips):
    results = []
    for ip in ips:
        try:
            data = track_ip(ip)
            results.append(data)
        except Exception as e:
            results.append({"ip": ip, "error": str(e)})
    return results


def bulk_phone_lookup(phones):
    results = []
    for phone in phones:
        try:
            data = track_phone(phone)
            results.append(data)
        except Exception as e:
            results.append({"phone": phone, "error": str(e)})
    return results
