# lego_blocks/load_data.py

import streamlit as st
import pandas as pd

def render():
    st.subheader("📥 Cargar archivo CSV")
    uploaded_file = st.file_uploader("Selecciona un archivo", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.success("Datos cargados correctamente ✅")
        st.write(df.head())
    elif "df" not in st.session_state:
        st.warning("Aún no se ha cargado ningún archivo.")
