# Standard Library Imports
# Third Party Imports
from os.path import join
from yaml import FullLoader, load
# Local Imports


# ==============================================================
# Import Settings From config.yaml
# ==============================================================
def import_config_settings() -> dict:
    """Import yaml file as dictionary"""
    try:
        with open('config.yaml', 'r') as f:
            result = load(f, Loader=FullLoader)
    except FileNotFoundError:
        with open(join('..', '..', 'config.yaml'), 'r') as f:
            result = load(f, Loader=FullLoader)
    return result


# ==============================================================
# Make settings variable available for import
# ==============================================================
SETTINGS = import_config_settings()
