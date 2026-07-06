"""
Entry point for `python -m ghosttrackerpro`.
"""

import sys

if __name__ == '__main__':
    from ghosttrackerpro.cli import main
    sys.exit(main())
