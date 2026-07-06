"""
GhostTrackerPro - Flask Web Application
Thin re-export from the ghosttrackerpro package.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghosttrackerpro.app import app

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    print(f"\n[*] GhostTrackerPro Web Interface")
    print(f"[*] Local:   http://localhost:{port}")
    print(f"[*] Press Ctrl+C to stop.\n")
    app.run(host=host, port=port, debug=False)
