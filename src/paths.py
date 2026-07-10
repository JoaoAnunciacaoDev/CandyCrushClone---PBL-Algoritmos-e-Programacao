import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_asset_path(*paths):
    """
    Resolve paths relative to the assets/ directory.
    """
    return os.path.join(BASE_DIR, "assets", *paths)
