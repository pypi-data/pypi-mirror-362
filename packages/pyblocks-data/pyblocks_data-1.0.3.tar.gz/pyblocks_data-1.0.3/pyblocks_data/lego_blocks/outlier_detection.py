# lego_blocks/outlier_detection.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px

def detect_zscore(df, col, threshold=3):
    """Detecta outliers usando Z-Score en una columna"""
    mean = df[col].mean()
    std = df[col].std()
    z_scores = (df[col] - mean) / std
    return df[np.abs(z_scores) > threshold]

def detect_iqr(df, col):
    """Detecta outliers usando el rango intercuartílico (IQR)"""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col] < lower_bound) | (df[col] > upper_bound)]

def detect_isolation_forest(df, cols, contamination=0.05):
    """Detecta anomalías multivariadas con Isolation Forest"""
    iso = IsolationForest(contamination=contamination, random_state=42)
    preds = iso.fit_predict(df[cols])
    return df[preds == -1]  # -1 = anomalía

def render():
    st.subheader("🚨 Detección de Outliers y Anomalías Avanzada")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    # Selección de columnas numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        st.error("No hay columnas numéricas para analizar.")
        return

    st.markdown("### 🔧 Configuración")
    method = st.radio(
        "Selecciona el método de detección:",
        ["Z-Score (univariante)", "IQR (univariante)", "Isolation Forest (multivariante)"]
    )
    selected_cols = st.multiselect("Selecciona columnas para analizar", num_cols, default=num_cols[:2])

    # Parámetro opcional para Isolation Forest
    contamination = 0.05
    if method == "Isolation Forest (multivariante)":
        contamination = st.slider("Nivel de sensibilidad (proporción de anomalías esperadas)", 0.01, 0.2, 0.05)

    if not selected_cols:
        st.warning("Selecciona al menos una columna.")
        return

    if st.button("🔍 Detectar anomalías"):
        if method.startswith("Z-Score"):
            anomalies = pd.DataFrame()
            for col in selected_cols:
                anomalies = pd.concat([anomalies, detect_zscore(df, col)], axis=0).drop_duplicates()
        elif method.startswith("IQR"):
            anomalies = pd.DataFrame()
            for col in selected_cols:
                anomalies = pd.concat([anomalies, detect_iqr(df, col)], axis=0).drop_duplicates()
        else:  # Isolation Forest
            anomalies = detect_isolation_forest(df, selected_cols, contamination)

        st.markdown(f"### ✅ Se detectaron **{anomalies.shape[0]} anomalías**")

        if anomalies.empty:
            st.info("No se detectaron anomalías según el método seleccionado.")
        else:
            st.dataframe(anomalies)

            # Visualización interactiva si hay al menos 2 columnas
            if len(selected_cols) >= 2:
                x_col, y_col = selected_cols[:2]
                df_plot = df.copy()
                df_plot["Anomalía"] = "Normal"
                df_plot.loc[df_plot.index.isin(anomalies.index), "Anomalía"] = "Anómala"

                fig = px.scatter(
                    df_plot, x=x_col, y=y_col,
                    color="Anomalía",
                    title="Mapa interactivo de anomalías",
                    symbol="Anomalía"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Exportar anomalías
            csv = anomalies.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Descargar anomalías en CSV",
                data=csv,
                file_name="anomalías_detectadas.csv"
            )

