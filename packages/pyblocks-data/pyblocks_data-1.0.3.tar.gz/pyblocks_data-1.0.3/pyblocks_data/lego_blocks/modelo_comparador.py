import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score, mean_squared_error,
    accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import matplotlib.pyplot as plt

def plot_radar(df, is_classification=True):
    categories = list(df.columns[1:])
    N = len(categories)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # cerrar la figura

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i in range(len(df)):
        values = df.iloc[i, 1:].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, label=df.iloc[i, 0])
        ax.fill(angles, values, alpha=0.1)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_rlabel_position(0)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    ax.set_title("Comparación de Modelos (Radar)", y=1.1)

    st.pyplot(fig)

def render():
    st.subheader("📊 Comparador de Modelos")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo primero.")
        return

    df = st.session_state["df"]

    target = st.selectbox("🎯 Selecciona la variable objetivo", df.columns)

    if target:
        X = df.drop(columns=[target])
        y = df[target]

        # Solo columnas numéricas o categóricas
        X = pd.get_dummies(X.select_dtypes(include=['number', 'category', 'object']), drop_first=True)

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        except:
            st.error("No se pudo dividir el dataset.")
            return

        is_classification = y.nunique() < 10 and y.dtype in ['int', 'object', 'category']

        st.markdown(f"🔍 Detectado como problema de **{'clasificación' if is_classification else 'regresión'}**")

        results = []

        if is_classification:
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier()
            }
        else:
            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor()
            }

        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                if is_classification:
                    results.append({
                        "Modelo": name,
                        "Accuracy": accuracy_score(y_test, y_pred),
                        "Precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
                        "Recall": recall_score(y_test, y_pred, average="weighted"),
                        "F1 Score": f1_score(y_test, y_pred, average="weighted")
                    })
                else:
                    results.append({
                        "Modelo": name,
                        "R2 Score": r2_score(y_test, y_pred),
                        "RMSE": mean_squared_error(y_test, y_pred, squared=False)
                    })

            except Exception as e:
                st.warning(f"No se pudo entrenar {name}: {e}")

        if results:
            df_results = pd.DataFrame(results)
            st.dataframe(df_results.style.format(precision=3))

            st.markdown("### 🕸️ Radar Comparativo de Métricas")
            plot_radar(df_results, is_classification)
