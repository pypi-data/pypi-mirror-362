# lego_blocks/pca_dimensionality.py

import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def render():
    st.subheader("🧬 Reducción de Dimensionalidad (PCA)")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]
    num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

    if len(num_cols) < 2:
        st.info("Se necesitan al menos dos columnas numéricas.")
        return

    st.markdown("### 🧹 Normalización de variables")
    if st.checkbox("Normalizar con StandardScaler (recomendado)", value=True):
        scaler = StandardScaler()
        X = scaler.fit_transform(df[num_cols])
    else:
        X = df[num_cols].values

    n_components = st.slider("¿Cuántos componentes principales?", 1, min(len(num_cols), 10), 2)

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)

    # Mostrar varianza explicada
    explained_var = pca.explained_variance_ratio_
    st.markdown("### 📈 Varianza explicada por componente")
    for i, var in enumerate(explained_var):
        st.write(f"PC{i+1}: {var:.2%}")

    # Visualizar los dos primeros componentes
    if n_components >= 2:
        st.markdown("### 📊 Visualización 2D (PC1 vs PC2)")
        pca_df = pd.DataFrame(components[:, :2], columns=["PC1", "PC2"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=pca_df, x="PC1", y="PC2", ax=ax)
        st.pyplot(fig)

    # Guardar en el dataframe actual
    pca_df_full = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)])
    df_pca = pd.concat([df.reset_index(drop=True), pca_df_full], axis=1)
    st.session_state["df"] = df_pca

    st.markdown("### 👀 Vista previa con componentes añadidos")
    st.dataframe(df_pca.head())
