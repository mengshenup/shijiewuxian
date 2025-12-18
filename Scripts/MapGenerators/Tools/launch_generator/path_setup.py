"""
Path setup module - ensures correct working directory
"""

import os
import sys
from pathlib import Path


def setup_paths():
    """Setup working directory and sys.path"""
    try:
        # Handle __file__ might not exist (e.g. when run via exec())
        if '__file__' in globals():
            script_dir = Path(__file__).parent.absolute()
        else:
            # If __file__ doesn't exist, infer from current working directory
            script_dir = Path.cwd() / 'Scripts' / 'MapGenerators' / 'Tools' / 'launch_generator'
        
        # Go up to project root: Tools/launch_generator -> MapGenerators -> Scripts -> project_root
        project_root = script_dir.parent.parent.parent.parent
        os.chdir(project_root)
        sys.path.insert(0, str(script_dir))
        
        print(f"[DEBUG] Working directory: {os.getcwd()}")
        print(f"[DEBUG] Script directory: {script_dir}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Path setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
