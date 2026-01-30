#!/usr/bin/env python3
"""
JStack Analyzer - Main entry point
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

try:
    from jstack_analyzer import main as analyzer_main
except ImportError:
    print("Error: Could not import jstack_analyzer module")
    sys.exit(1)

if __name__ == '__main__':
    analyzer_main()