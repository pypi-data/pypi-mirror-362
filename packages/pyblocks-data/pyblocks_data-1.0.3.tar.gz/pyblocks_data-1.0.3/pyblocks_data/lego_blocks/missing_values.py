# lego_blocks/missing_values.py

# lego_blocks/missing_values.py

import streamlit as st
import pandas as pd

def render():
    st.subheader("🚫 Manejo de Valores Nulos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    st.markdown("### 🧮 Conteo de nulos por columna")
    null_counts = df.isnull().sum()
    st.dataframe(null_counts[null_counts > 0].to_frame(name="Valores Nulos"))

    if null_counts.sum() == 0:
        st.success("✅ No hay valores nulos en el dataset.")
        return

    st.markdown("### 🛠️ Acciones disponibles")

    action = st.selectbox("¿Qué deseas hacer con los valores nulos?", [
        "No hacer nada",
        "Eliminar filas con nulos",
        "Rellenar con la media",
        "Rellenar con la mediana",
        "Rellenar con un valor personalizado"
    ])

    if action == "Eliminar filas con nulos":
        df = df.dropna()
        st.success("Se eliminaron las filas con valores nulos.")

    elif action == "Rellenar con la media":
        df = df.fillna(df.mean(numeric_only=True))
        st.success("Se rellenaron los valores nulos con la media.")

    elif action == "Rellenar con la mediana":
        df = df.fillna(df.median(numeric_only=True))
        st.success("Se rellenaron los valores nulos con la mediana.")

    elif action == "Rellenar con un valor personalizado":
        columnas = df.columns[df.isnull().any()].tolist()
        col = st.selectbox("Selecciona la columna a rellenar", columnas)
        custom_value = st.text_input("Valor con el que rellenar (como texto):")
        if st.button("Aplicar"):
            df[col] = df[col].fillna(custom_value)
            st.success(f"Columna '{col}' rellenada con: {custom_value}")

    st.session_state["df"] = df

    st.markdown("### 📋 Vista previa después del tratamiento")
    st.dataframe(df.head())

