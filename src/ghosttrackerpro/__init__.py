"""
GhostTrackerPro - Professional OSINT Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A full-stack OSINT reconnaissance and educational tracking platform
for cybersecurity professionals and ethical hackers.

Modules:
  - IP Address Intelligence
  - Phone Number Analysis
  - Username OSINT (20 platforms)
  - Subdomain Enumeration
  - DNS Lookup
  - WHOIS Lookup
  - Port Scanner
  - URL / Header Analyzer
  - SSL Certificate Checker
  - Hash Lookup
  - Email Breach Check
  - IP Reputation
  - Bulk IP/Phone Lookup
  - Live GPS Tracker
  - Web Interface

Usage:
  ghosttrackerpro              # Interactive CLI menu
  ghosttrackerpro --ip 8.8.8.8 # Direct lookup
  ghosttrackerpro --web        # Start web interface
  python -m ghosttrackerpro    # Same as above
"""

__version__ = "2.0.0"
__author__ = "HUNXBYTS"
__license__ = "Educational Use Only"

from ghosttrackerpro.core import (
    track_ip,
    track_phone,
    track_username,
    get_my_ip,
    get_local_ip,
    save_result,
    read_logs,
    enumerate_subdomains,
    dns_lookup,
    email_breach_check,
    hash_lookup,
    port_scan,
    whois_lookup,
    analyze_url,
    ssl_check,
    ip_reputation,
    bulk_ip_lookup,
    bulk_phone_lookup,
    ensure_logs_dir,
)

__all__ = [
    'track_ip', 'track_phone', 'track_username', 'get_my_ip', 'get_local_ip',
    'save_result', 'read_logs', 'enumerate_subdomains', 'dns_lookup',
    'email_breach_check', 'hash_lookup', 'port_scan', 'whois_lookup',
    'analyze_url', 'ssl_check', 'ip_reputation', 'bulk_ip_lookup',
    'bulk_phone_lookup', 'ensure_logs_dir',
]
