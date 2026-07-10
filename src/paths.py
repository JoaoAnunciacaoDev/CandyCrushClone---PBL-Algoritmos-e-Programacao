import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    EXE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    EXE_DIR = BASE_DIR

def get_asset_path(*paths):
    """
    Resolve paths relative to the assets/ directory.
    """
    return os.path.join(BASE_DIR, "assets", *paths)

def get_save_path(filename):
    """
    Resolve paths for save/data files (e.g. scoreboard) in the executable's folder.
    """
    return os.path.join(EXE_DIR, filename)
