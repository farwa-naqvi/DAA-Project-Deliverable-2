
import os
import sys
import streamlit.web.cli as stcli

project_folder = os.path.dirname(os.path.abspath(__file__))
ui_folder = os.path.join(project_folder, "ui")

sys.path.append(ui_folder)

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", os.path.join(ui_folder, "dashboard.py")]
    sys.exit(stcli.main())
