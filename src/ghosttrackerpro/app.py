import os
import sys

from flask import Flask, request, jsonify, render_template, send_from_directory

from ghosttrackerpro.core import (
    track_ip, track_phone, track_username, get_my_ip,
    get_local_ip, save_result, read_logs,
    enumerate_subdomains, dns_lookup, email_breach_check,
    hash_lookup, port_scan, whois_lookup, analyze_url,
    ssl_check, ip_reputation, bulk_ip_lookup, bulk_phone_lookup,
)

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')

app = Flask(__name__, template_folder=os.path.join(WEB_DIR, 'templates'), static_folder=None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'static'), filename)


@app.route('/')
def index():
    return render_template('index.html')


# -----------------------------------------------------------------------
# Existing core endpoints
# -----------------------------------------------------------------------

@app.route('/api/my-ip')
def api_my_ip():
    try:
        data = get_my_ip()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/ip-track', methods=['POST'])
def api_ip_track():
    ip = request.json.get('ip', '').strip()
    if not ip:
        return jsonify({"success": False, "error": "IP address is required"}), 400
    try:
        data = track_ip(ip)
        log = (
            f"IP: {data['ip']}\n"
            f"Country: {data['country']}\n"
            f"City: {data['city']}\n"
            f"Region: {data['region']}\n"
            f"ISP: {data['isp']}\n"
            f"Organization: {data['organization']}\n"
            f"Coordinates: {data['latitude']}, {data['longitude']}"
        )
        saved = save_result("IP_TRACK", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/phone-track', methods=['POST'])
def api_phone_track():
    phone = request.json.get('phone', '').strip()
    if not phone:
        return jsonify({"success": False, "error": "Phone number is required"}), 400
    try:
        data = track_phone(phone)
        log = (
            f"Phone: {data['phone']}\n"
            f"Country Code: {data['country_code']}\n"
            f"National: {data['national_number']}\n"
            f"Location: {data['location']}\n"
            f"Carrier: {data['carrier']}\n"
            f"Timezone: {data['timezone']}\n"
            f"Valid: {data['is_valid']}"
        )
        saved = save_result("PHONE_TRACK", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/username-track', methods=['POST'])
def api_username_track():
    username = request.json.get('username', '').strip()
    if not username:
        return jsonify({"success": False, "error": "Username is required"}), 400
    try:
        data = track_username(username)
        found = [r for r in data['results'] if r['status'] == 'found']
        log = f"Username: {username}\n\nFound on:\n" + "\n".join(f"{r['platform']}: {r['url']}" for r in found)
        blocked = [r for r in data['results'] if r['status'] in ('blocked', 'rate_limited')]
        not_found = [r for r in data['results'] if r['status'] in ('not_found', 'error', 'timeout')]
        if not_found:
            log += "\n\nNot found on:\n" + "\n".join(r['platform'] for r in not_found)
        if blocked:
            log += "\n\nBlocked/Error on:\n" + "\n".join(r['platform'] for r in blocked)
        saved = save_result("USERNAME_TRACK", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/logs')
def api_logs():
    try:
        entries = read_logs()
        return jsonify({"success": True, "data": entries})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------------------------------------------
# New endpoints
# -----------------------------------------------------------------------

@app.route('/api/subdomain-enum', methods=['POST'])
def api_subdomain_enum():
    domain = request.json.get('domain', '').strip()
    if not domain:
        return jsonify({"success": False, "error": "Domain is required"}), 400
    try:
        data = enumerate_subdomains(domain)
        log = f"Domain: {domain}\nSubdomains found: {data['count']}\n\n" + "\n".join(data['subdomains']) if data['subdomains'] else "No subdomains found"
        saved = save_result("SUBDOMAIN_ENUM", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/dns-lookup', methods=['POST'])
def api_dns_lookup():
    domain = request.json.get('domain', '').strip()
    if not domain:
        return jsonify({"success": False, "error": "Domain is required"}), 400
    try:
        data = dns_lookup(domain)
        records = data['records']
        log = f"DNS Records for: {domain}\n\n"
        for rtype, values in records.items():
            log += f"[{rtype}]\n"
            for v in values:
                log += f"  {v}\n"
            if not values:
                log += "  (no records found)\n"
            log += "\n"
        saved = save_result("DNS_LOOKUP", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/email-breach', methods=['POST'])
def api_email_breach():
    email = request.json.get('email', '').strip()
    if not email:
        return jsonify({"success": False, "error": "Email is required"}), 400
    try:
        data = email_breach_check(email)
        log = f"Email: {email}\nCompromised: {data.get('compromised', 'Unknown')}\n"
        if data.get('breaches'):
            log += f"\nBreaches found: {len(data['breaches'])}\n"
            for b in data['breaches']:
                log += f"  - {b.get('source')}: {b.get('count', '?')} occurrences\n"
        saved = save_result("EMAIL_BREACH", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/hash-lookup', methods=['POST'])
def api_hash_lookup():
    hash_val = request.json.get('hash', '').strip()
    if not hash_val:
        return jsonify({"success": False, "error": "Hash value is required"}), 400
    try:
        data = hash_lookup(hash_val)
        log = f"Hash: {hash_val}\nType: {data.get('type', 'Unknown')}\nFound: {data['found']}\n"
        if data.get('plaintext'):
            log += f"Plaintext: {data['plaintext']}\n"
        saved = save_result("HASH_LOOKUP", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/port-scan', methods=['POST'])
def api_port_scan():
    host = request.json.get('host', '').strip()
    if not host:
        return jsonify({"success": False, "error": "Host is required"}), 400
    try:
        data = port_scan(host)
        log = f"Port Scan Results for: {host}\n\n"
        for p in data['open_ports']:
            log += f"  Port {p['port']}/tcp  OPEN  {p.get('service', '')}\n"
        if not data['open_ports']:
            log += "  No open ports found among common ports.\n"
        log += f"\nScanned: {data['ports_scanned']} ports\nOpen: {data['total_open']}"
        saved = save_result("PORT_SCAN", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/whois', methods=['POST'])
def api_whois():
    domain = request.json.get('domain', '').strip()
    if not domain:
        return jsonify({"success": False, "error": "Domain is required"}), 400
    try:
        data = whois_lookup(domain)
        d = data['data']
        log = f"WHOIS for: {domain}\n\n"
        log += f"Domain: {d.get('domain', 'N/A')}\n"
        log += f"Registrant: {d.get('registrant', 'N/A')}\n"
        log += f"Created: {d.get('creation_date', 'N/A')}\n"
        log += f"Expires: {d.get('expiration_date', 'N/A')}\n"
        log += f"Last Changed: {d.get('last_changed', 'N/A')}\n"
        log += f"DNSSEC: {d.get('dnssec', 'N/A')}\n"
        if d.get('nameservers'):
            log += "\nNameservers:\n" + "\n".join(f"  {ns}" for ns in d['nameservers'])
        saved = save_result("WHOIS", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/url-analyze', methods=['POST'])
def api_url_analyze():
    url = request.json.get('url', '').strip()
    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400
    try:
        data = analyze_url(url)
        sec = data.get('security_headers', {})
        log = f"URL Analysis: {url}\n\n"
        log += f"Final URL: {data.get('final_url', 'N/A')}\n"
        log += f"Status: {data.get('status_code', 'N/A')}\n"
        log += f"Server: {data.get('server', 'N/A')}\n"
        log += f"Content-Type: {data.get('content_type', 'N/A')}\n"
        log += f"Redirects: {data.get('redirect_count', 0)}\n\n"
        log += "Security Headers:\n"
        if sec:
            for k, v in sec.items():
                log += f"  {k}: {v}\n"
        else:
            log += "  None found\n"
        saved = save_result("URL_ANALYSIS", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/ssl-check', methods=['POST'])
def api_ssl_check():
    hostname = request.json.get('hostname', '').strip()
    if not hostname:
        return jsonify({"success": False, "error": "Hostname is required"}), 400
    try:
        data = ssl_check(hostname)
        log = f"SSL Certificate Check for: {hostname}\n\n"
        log += f"Valid: {data['valid']}\n"
        log += f"Subject: {data.get('subject', 'N/A')}\n"
        log += f"Issuer: {data.get('issuer', 'N/A')}\n"
        log += f"Issued: {data.get('issued', 'N/A')}\n"
        log += f"Expires: {data.get('expiry', 'N/A')}\n"
        log += f"Version: {data.get('version', 'N/A')}\n"
        if data.get('error'):
            log += f"Error: {data['error']}\n"
        saved = save_result("SSL_CHECK", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/ip-reputation', methods=['POST'])
def api_ip_reputation():
    ip = request.json.get('ip', '').strip()
    if not ip:
        return jsonify({"success": False, "error": "IP address is required"}), 400
    try:
        data = ip_reputation(ip)
        log = f"IP Reputation: {ip}\n\n"
        log += f"VPN: {data['is_vpn']}\n"
        log += f"Proxy: {data['is_proxy']}\n"
        log += f"TOR: {data['is_tor']}\n"
        log += f"Threat Level: {data.get('threat', 'unknown')}\n"
        saved = save_result("IP_REPUTATION", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bulk-ip', methods=['POST'])
def api_bulk_ip():
    ips = request.json.get('ips', [])
    if not ips or not isinstance(ips, list):
        return jsonify({"success": False, "error": "List of IPs is required"}), 400
    try:
        data = bulk_ip_lookup(ips)
        log = "Bulk IP Lookup\n\n" + "\n".join(f"{d.get('ip', '?')}: {d.get('country', 'error')}" for d in data)
        saved = save_result("BULK_IP", log)
        return jsonify({"success": True, "data": data, "_saved": saved})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bulk-phone', methods=['POST'])
def api_bulk_phone():
    phones = request.json.get('phones', [])
    if not phones or not isinstance(phones, list):
        return jsonify({"success": False, "error": "List of phone numbers is required"}), 400
    try:
        data = bulk_phone_lookup(phones)
        log = "Bulk Phone Lookup\n\n" + "\n".join(f"{d.get('phone', '?')}: {d.get('location', 'error')}" for d in data)
        saved = save_result("BULK_PHONE", log)
        return jsonify({"success": True, "data": data, "_saved": saved})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    print(f"\n[*] GhostTrackerPro Web Interface")
    print(f"[*] Local:   http://localhost:{port}")
    print(f"[*] Press Ctrl+C to stop.\n")
    app.run(host=host, port=port, debug=False)
