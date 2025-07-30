# lego_blocks/project_summary.py

import streamlit as st
import json
from io import BytesIO

def render():
    st.subheader("📊 Resumen del Proyecto LEGO")

    bloques_usados = st.session_state.get("bloques_usados", [])
    archivo_csv = st.session_state.get("csv_filename", "No cargado")
    notas = st.session_state.get("notas_proyecto", "")
    reporte_html = st.session_state.get("sweetviz_report_path", "No generado")

    st.markdown("### 🧱 Bloques utilizados")
    if bloques_usados:
        for bloque in bloques_usados:
            st.write(f"✔️ {bloque}")
    else:
        st.info("Aún no se ha utilizado ningún bloque.")

    st.markdown("### 📁 Archivo CSV cargado")
    st.write(archivo_csv)

    st.markdown("### 🌐 Reporte Sweetviz generado")
    st.write(reporte_html if reporte_html else "No generado")

    st.markdown("### 📝 Notas del proyecto")
    notas_input = st.text_area("Agrega tus notas aquí:", value=notas)
    st.session_state["notas_proyecto"] = notas_input

    st.markdown("### 📦 Exportar proyecto")
    if st.button("Descargar JSON con el resumen"):
        resumen = {
            "bloques_usados": bloques_usados,
            "archivo_csv": archivo_csv,
            "notas": notas_input,
            "reporte_html": reporte_html,
        }
        buffer = BytesIO()
        buffer.write(json.dumps(resumen, indent=4).encode("utf-8"))
        st.download_button(
            label="⬇️ Descargar resumen",
            data=buffer.getvalue(),
            file_name="proyecto_LEGO.json",
            mime="application/json"
        )
