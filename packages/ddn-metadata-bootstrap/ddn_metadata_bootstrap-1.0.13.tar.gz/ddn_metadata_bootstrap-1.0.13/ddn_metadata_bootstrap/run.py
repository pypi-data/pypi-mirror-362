#!/usr/bin/env python3

"""
Direct execution script for Metadata Bootstrap.
This script can be run directly without module imports.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main function
from .main import main

if __name__ == "__main__":
    main()
