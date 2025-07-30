import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def render():
    st.subheader("📈 Análisis de Series Temporales")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    st.markdown("### 🔧 Configuración de la Serie Temporal")

    date_col = st.selectbox("Selecciona la columna de fecha:", df.columns)
    value_col = st.selectbox("Selecciona la columna de valores:", df.select_dtypes(include=["float64", "int64"]).columns)

    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(by=date_col)
        df.set_index(date_col, inplace=True)
    except Exception as e:
        st.error(f"Error al convertir la columna de fecha: {e}")
        return

    st.line_chart(df[value_col])

    st.markdown("### 🧠 Descomposición Estacional")

    freq = st.selectbox("Frecuencia de la serie:", ["D", "W", "M", "Q", "Y"], index=2)

    try:
        result = seasonal_decompose(df[value_col], model="additive", period={"D": 7, "W": 4, "M": 12, "Q": 4, "Y": 1}[freq])
        fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
        result.observed.plot(ax=axes[0], title="Observado")
        result.trend.plot(ax=axes[1], title="Tendencia")
        result.seasonal.plot(ax=axes[2], title="Estacionalidad")
        result.resid.plot(ax=axes[3], title="Residual")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al descomponer la serie: {e}")
