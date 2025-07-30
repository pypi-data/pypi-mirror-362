# clustering.py

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def render():
    st.subheader("🔄 Clustering con K-Means")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if len(numeric_cols) < 2:
        st.error("Se necesitan al menos dos columnas numéricas para clustering.")
        return

    st.markdown("### 🔢 Selección de variables para clustering")
    selected_cols = st.multiselect("Selecciona columnas numéricas", numeric_cols, default=numeric_cols)

    if not selected_cols:
        st.info("Selecciona al menos dos variables.")
        return

    X = df[selected_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Número de clusters (k)", 2, 10, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    df_clusters = df.copy()
    df_clusters["Cluster"] = clusters

    st.markdown("### 📊 Visualización 2D (PCA)")
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    comp_df = pd.DataFrame(components, columns=["Componente 1", "Componente 2"])
    comp_df["Cluster"] = clusters

    fig, ax = plt.subplots()
    sns.scatterplot(data=comp_df, x="Componente 1", y="Componente 2", hue="Cluster", palette="Set2", ax=ax)
    st.pyplot(fig)

    st.markdown("### 🧾 Resultados")
    st.write(df_clusters.head())

    st.download_button(
        label="📥 Descargar CSV con Clusters",
        data=df_clusters.to_csv(index=False).encode("utf-8"),
        file_name="datos_con_clusters.csv",
        mime="text/csv"
    )

    # Guardar en sesión por si se quiere usar luego
    st.session_state["df"] = df_clusters
