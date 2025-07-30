import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def render():
    st.subheader("🎯 Selección de Variables + Preprocesamiento")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo primero.")
        return

    df = st.session_state["df"]
    st.dataframe(df.head())

    # Selección de variables
    target = st.selectbox("📌 Variable objetivo", df.columns)
    predictors = st.multiselect("🧠 Variables predictoras", [col for col in df.columns if col != target])

    if not predictors or not target:
        st.info("Selecciona al menos una variable predictora y una objetivo.")
        return

    st.session_state["target_variable"] = target
    st.session_state["predictor_variables"] = predictors

    # ¿Aplicar preprocesamiento?
    apply_preprocessing = st.checkbox("⚙️ Aplicar preprocesamiento automático", value=True)

    if apply_preprocessing:
        df_model = df[predictors + [target]].copy()

        # Separar X y y
        X = df_model[predictors]
        y = df_model[target]

        # Detectar columnas numéricas y categóricas
        num_cols = X.select_dtypes(include=["int", "float"]).columns.tolist()
        cat_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

        st.markdown(f"🔢 Variables numéricas: {', '.join(num_cols) if num_cols else 'Ninguna'}")
        st.markdown(f"🔤 Variables categóricas: {', '.join(cat_cols) if cat_cols else 'Ninguna'}")

        # Pipelines de preprocesamiento
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ])

        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])

        preprocessor = ColumnTransformer([
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols)
        ])

        # Aplicar transformación
        X_processed = preprocessor.fit_transform(X)
        X_processed_df = pd.DataFrame(X_processed,
                                      columns=preprocessor.get_feature_names_out(),
                                      index=X.index)

        # Guardar resultados
        st.session_state["X_processed"] = X_processed_df
        st.session_state["y"] = y

        st.success("✅ Preprocesamiento aplicado correctamente")
        st.dataframe(X_processed_df.head())

    else:
        st.warning("Preprocesamiento no aplicado. Solo se guardan variables seleccionadas.")
        st.session_state["X_processed"] = df[predictors]
        st.session_state["y"] = df[target]
