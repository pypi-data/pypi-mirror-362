# lego_blocks/basic_stats.py

# basic_stats.py

import streamlit as st
import pandas as pd
from pyblocks_data.utils.helpers import lego_card

def render():
    st.subheader("📊 Estadísticas Básicas")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo primero.")
        return

    df = st.session_state["df"]

    # 💠 Visual LEGO: bloques con colores
    lego_card("Vista previa", "👀", "#D1F2EB", df.head().to_html(index=False))

    lego_card("Dimensiones", "📏", "#ABEBC6", f"Filas: {df.shape[0]}<br>Columnas: {df.shape[1]}")

    lego_card("Tipos de datos", "📋", "#F9E79F", df.dtypes.to_frame().to_html())

    lego_card("Estadísticas", "📉", "#FADBD8", df.describe().to_html())

    lego_card("Valores nulos", "🚫", "#D6EAF8", df.isnull().sum().to_frame().to_html())

