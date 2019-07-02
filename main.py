# Standard Library Imports
import sys
# Third Party Imports
# Local Imports
from src.app import App


# ==============================================================
# Main
# ==============================================================
if __name__ == "__main__":
    app = App()
    sys.exit(app.app.exec_())


