import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score
)

def render():
    st.subheader("🧪 Evaluación de Modelos")

    if "model_results" not in st.session_state:
        st.warning("Primero entrena un modelo para evaluarlo.")
        return

    results = st.session_state["model_results"]  # {nombre_modelo: (modelo, X_test, y_test)}

    for name, (model, X_test, y_test) in results.items():
        st.markdown(f"## 🔍 Modelo: `{name}`")
        y_pred = model.predict(X_test)

        # Clasificación o regresión
        if pd.api.types.is_numeric_dtype(y_test) and len(np.unique(y_test)) > 10:
            st.markdown("### 📏 Métricas de Regresión")
            mae = mean_absolute_error(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            r2 = r2_score(y_test, y_pred)

            st.write(f"**MAE:** {mae:.4f}")
            st.write(f"**RMSE:** {rmse:.4f}")
            st.write(f"**R²:** {r2:.4f}")

            fig, ax = plt.subplots()
            sns.scatterplot(x=y_test, y=y_pred, ax=ax)
            ax.set_xlabel("Reales")
            ax.set_ylabel("Predichos")
            ax.set_title("Reales vs Predichos")
            st.pyplot(fig)

        else:
            st.markdown("### 📊 Métricas de Clasificación")
            acc = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

            st.write(f"**Accuracy:** {acc:.4f}")
            st.write(f"**Precisión:** {precision:.4f}")
            st.write(f"**Recall:** {recall:.4f}")
            st.write(f"**F1 Score:** {f1:.4f}")

            st.text("📋 Reporte de Clasificación:")
            st.text(classification_report(y_test, y_pred, zero_division=0))

            st.markdown("### 📌 Matriz de Confusión")
            cm = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", ax=ax)
            ax.set_xlabel("Predicción")
            ax.set_ylabel("Real")
            st.pyplot(fig)
