import subprocess
import sys
import os

def main():
    # app.py ahora está junto a cli.py
    ruta_app = os.path.join(os.path.dirname(__file__), "app.py")

    comando = [sys.executable, "-m", "streamlit", "run", ruta_app] + sys.argv[1:]
    subprocess.run(comando)
