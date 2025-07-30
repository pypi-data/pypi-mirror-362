# lego_blocks/transformations.py

import streamlit as st
import pandas as pd

def render():
    st.subheader("🧼 Transformaciones y Limpieza de Datos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    # Selección de columnas
    st.markdown("### 🔍 Seleccionar columnas")
    selected_columns = st.multiselect("Elige las columnas que quieres conservar", df.columns.tolist(), default=df.columns.tolist())

    if selected_columns:
        df = df[selected_columns]

    # Filtrado por valor
    st.markdown("### 🔽 Filtrar datos por columna")
    filter_column = st.selectbox("Selecciona una columna para filtrar", df.columns.tolist())
    unique_vals = df[filter_column].unique().tolist()
    selected_val = st.selectbox("Selecciona un valor", unique_vals)
    if st.button("Aplicar filtro"):
        df = df[df[filter_column] == selected_val]
        st.success(f"Filtro aplicado: {filter_column} = {selected_val}")

    # Eliminar valores nulos
    if st.checkbox("🗑️ Eliminar filas con valores nulos"):
        df = df.dropna()
        st.success("Filas con valores nulos eliminadas.")

    st.session_state["df"] = df  # Actualiza el dataframe procesado

    st.markdown("### 📋 Vista previa del DataFrame transformado")
    st.dataframe(df.head())
