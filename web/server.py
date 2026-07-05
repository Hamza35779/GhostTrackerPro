import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, render_template, send_from_directory

from core import (
    track_ip, track_phone, track_username, get_my_ip,
    get_local_ip, save_result, read_logs
)

WEB_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(WEB_DIR, 'templates'), static_folder=None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'static'), filename)


@app.route('/')
def index():
    return render_template('index.html')


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
        blocked = [r for r in data['results'] if r['status'] == 'blocked']
        not_found = [r for r in data['results'] if r['status'] in ('not_found', 'error')]
        if not_found:
            log += "\n\nNot found on:\n" + "\n".join(r['platform'] for r in not_found)
        if blocked:
            log += "\n\nBlocked/Error on:\n" + "\n".join(r['platform'] for r in blocked)
        saved = save_result("USERNAME_TRACK", log)
        data['_saved'] = saved
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/gps-server', methods=['POST'])
def api_gps_server():
    return jsonify({
        "success": True,
        "data": {
            "local_ip": get_local_ip(),
            "instructions": "The GPS tracker runs locally via: python3 GhostTrackerPro.py --gps"
        }
    })


@app.route('/api/logs')
def api_logs():
    try:
        entries = read_logs()
        return jsonify({"success": True, "data": entries})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    print(f"\n[*] GhostTrackerPro Web Interface")
    print(f"[*] Local:   http://localhost:{port}")
    print(f"[*] Press Ctrl+C to stop.\n")
    app.run(host=host, port=port, debug=False)
