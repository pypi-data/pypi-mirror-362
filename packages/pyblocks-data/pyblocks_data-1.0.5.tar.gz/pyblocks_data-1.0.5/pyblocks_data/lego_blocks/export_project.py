import streamlit as st
import pandas as pd
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

def render():
    st.subheader("💾 Exportar Proyecto")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    st.write("Descarga el DataFrame actual:")

    csv = df.to_csv(index=False).encode('utf-8')
    excel = to_excel(df)

    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="datos_exportados.csv",
        mime="text/csv"
    )

    st.download_button(
        label="📥 Descargar Excel",
        data=excel,
        file_name="datos_exportados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
