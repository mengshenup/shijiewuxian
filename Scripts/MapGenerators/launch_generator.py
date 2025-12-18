"""
Launch Generator - Entry Point
Monitors UE5 map generation with smart timeout and auto-retry

This is a modular refactored version.
The code is split into atomic modules in Tools/launch_generator/

Usage:
    python launch_generator.py [map_name]
    
    Example:
        python launch_generator.py cosmos_002_training_world
"""

import sys
from pathlib import Path

# Add Tools/launch_generator to path
tools_dir = Path(__file__).parent / "Tools" / "launch_generator"
sys.path.insert(0, str(tools_dir))

# Import and run main
from main import main

# Run main
if __name__ == "__main__":
    sys.exit(main())
