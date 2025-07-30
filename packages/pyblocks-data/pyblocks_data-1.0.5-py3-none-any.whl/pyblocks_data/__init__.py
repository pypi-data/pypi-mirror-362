def main():
    import os
    import pathlib

    # Ruta absoluta al app.py en la carpeta raíz del proyecto
    app_path = pathlib.Path(__file__).parent.parent / "app.py"
    
    print("DEBUG >>> Ruta calculada:", app_path.as_posix())
    
    if not app_path.exists():
        print("❌ ERROR: No se encontró app.py en", app_path)
        return
    
    # Ejecuta Streamlit con la ruta correcta
    os.system(f"streamlit run \"{app_path.as_posix()}\"")



