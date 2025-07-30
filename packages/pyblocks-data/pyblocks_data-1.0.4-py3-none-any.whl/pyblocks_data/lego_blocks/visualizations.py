# lego_blocks/visualizations.py

import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt

def render():
    st.subheader("📈 Visualización de Datos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

    st.markdown("Selecciona las variables que quieres visualizar:")
    chart_type = st.selectbox("Tipo de gráfico", ["Histograma", "Gráfico de Dispersión", "Mapa de Calor"])

    if chart_type == "Histograma":
        col1, col2 = st.columns([1, 2])
        with col1:
            column = st.selectbox("Columna numérica", cols)
            bins = st.slider("Cantidad de bins", 5, 100, 20)
        with col2:
            fig, ax = plt.subplots()
            sns.histplot(df[column], bins=bins, kde=True, ax=ax)
            st.pyplot(fig)

    elif chart_type == "Gráfico de Dispersión":
        col1, col2 = st.columns([1, 2])
        with col1:
            x = st.selectbox("Eje X", cols, key="x_scatter")
            y = st.selectbox("Eje Y", cols, key="y_scatter")
        with col2:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x, y=y, ax=ax)
            st.pyplot(fig)

    elif chart_type == "Mapa de Calor":
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("Este gráfico se genera automáticamente con las columnas numéricas del dataset.")
        with col2:
            fig, ax = plt.subplots()
            corr = df[cols].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)


