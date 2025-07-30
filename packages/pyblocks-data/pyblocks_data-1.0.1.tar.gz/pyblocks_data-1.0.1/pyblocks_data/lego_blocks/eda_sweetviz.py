# lego_blocks/eda_auto.py
# lego_blocks/eda_auto.py

# lego_blocks/eda_sweetviz.py

import streamlit as st
import sweetviz as sv
import pandas as pd
import tempfile
import os
import webbrowser

def render():
    st.subheader("📊 Análisis Exploratorio con Sweetviz")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    if st.button("🧠 Generar Reporte Sweetviz"):
        with st.spinner("Generando reporte..."):
            try:
                report = sv.analyze(df)

                # Archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                    report_path = f.name
                report.show_html(filepath=report_path, open_browser=False)

                # Guardar ruta para "flujo LEGO"
                st.session_state["sweetviz_report_path"] = report_path

                # Mostrar HTML embebido
                with open(report_path, "r", encoding="utf-8") as f:
                    html = f.read()
                st.components.v1.html(html, height=800, scrolling=True)

                # Botón para abrir en navegador externo
                if st.button("🌐 Abrir en el navegador"):
                    webbrowser.open_new_tab("file://" + report_path)

                # Botón para descargar
                with open(report_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar Reporte en HTML",
                        data=f,
                        file_name="reporte_sweetviz.html",
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"❌ Error generando el reporte: {e}")



