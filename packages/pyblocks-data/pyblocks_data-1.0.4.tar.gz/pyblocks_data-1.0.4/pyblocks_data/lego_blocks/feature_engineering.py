# lego_blocks/feature_engineering.py

import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

def render():
    st.subheader("🛠️ Ingeniería de Variables")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    st.markdown("### ➕ Crear nueva columna (operación entre columnas)")
    cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    if len(cols) >= 2:
        col1 = st.selectbox("Columna 1", cols, key="col1")
        operation = st.selectbox("Operación", ["+", "-", "*", "/"])
        col2 = st.selectbox("Columna 2", cols, key="col2")
        new_col_name = st.text_input("Nombre de la nueva columna")

        if st.button("Crear nueva columna"):
            try:
                if operation == "+":
                    df[new_col_name] = df[col1] + df[col2]
                elif operation == "-":
                    df[new_col_name] = df[col1] - df[col2]
                elif operation == "*":
                    df[new_col_name] = df[col1] * df[col2]
                elif operation == "/":
                    df[new_col_name] = df[col1] / df[col2]
                st.success(f"Columna '{new_col_name}' creada.")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### 🧩 Codificación de variables categóricas")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if cat_cols:
        cat_col = st.selectbox("Selecciona columna categórica", cat_cols)
        encoding = st.radio("Tipo de codificación", ["Label Encoding", "One-Hot Encoding"])

        if st.button("Aplicar codificación"):
            try:
                if encoding == "Label Encoding":
                    le = LabelEncoder()
                    df[cat_col + "_encoded"] = le.fit_transform(df[cat_col])
                    st.success(f"'{cat_col}' codificada con LabelEncoder.")
                else:
                    df = pd.get_dummies(df, columns=[cat_col])
                    st.success(f"'{cat_col}' convertida con One-Hot Encoding.")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### 📏 Escalado de variables numéricas")
    scale_cols = st.multiselect("Selecciona columnas numéricas a escalar", cols)

    scaler_type = st.radio("Tipo de escalado", ["MinMaxScaler", "StandardScaler"])
    if st.button("Aplicar escalado"):
        try:
            scaler = MinMaxScaler() if scaler_type == "MinMaxScaler" else StandardScaler()
            scaled = scaler.fit_transform(df[scale_cols])
            scaled_df = pd.DataFrame(scaled, columns=[col + "_scaled" for col in scale_cols])
            df = pd.concat([df, scaled_df], axis=1)
            st.success(f"Escalado aplicado con {scaler_type}.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.session_state["df"] = df

    st.markdown("### 👀 Vista previa actual del DataFrame")
    st.dataframe(df.head())
