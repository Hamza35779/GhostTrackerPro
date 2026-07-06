#!/usr/bin/env python3
"""
GhostTrackerPro - Professional OSINT Toolkit
Standalone CLI entry point. Delegates to the ghosttrackerpro package.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghosttrackerpro.cli import main

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n[+] Exiting...')
        sys.exit(0)
