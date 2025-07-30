# lego_blocks/correlation_analysis.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def render():
    st.subheader("📈 Análisis de Correlación")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=['float', 'int']).columns

    if len(num_cols) < 2:
        st.info("Se necesitan al menos dos columnas numéricas.")
        return

    st.markdown("### 🔗 Matriz de correlación (Pearson)")

    corr_matrix = df[num_cols].corr()
    st.dataframe(corr_matrix)

    st.markdown("### 🌡️ Mapa de Calor de Correlación")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.markdown("### 🎯 Correlación con una variable objetivo")
    target = st.selectbox("Selecciona variable objetivo", num_cols)
    sorted_corr = corr_matrix[target].sort_values(ascending=False)
    st.dataframe(sorted_corr.to_frame(name="Correlación con " + target))
