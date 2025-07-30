import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

def render():
    st.subheader("📆 Pronóstico y Comparación de Modelos (Prophet vs SARIMAX)")

    if "df" not in st.session_state:
        st.warning("Debes cargar un archivo CSV primero.")
        return

    df = st.session_state["df"]

    st.markdown("### ⚙️ Configuración Inicial")
    date_col = st.selectbox("Selecciona la columna de fecha:", df.columns)
    target_col = st.selectbox("Selecciona la variable a predecir:", df.columns)

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    # Dividimos Train/Test
    test_size = st.slider("Porcentaje de datos para prueba", 5, 50, 20)
    split_idx = int(len(df) * (1 - test_size / 100))
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    st.write(f"📊 **Entrenamiento:** {len(train_df)} filas | **Prueba:** {len(test_df)} filas")

    # Prophet
    prophet_df = train_df[[date_col, target_col]].rename(columns={date_col: "ds", target_col: "y"})
    prophet_model = Prophet()
    prophet_model.fit(prophet_df)

    future_test = test_df[[date_col]].rename(columns={date_col: "ds"})
    prophet_forecast = prophet_model.predict(future_test)

    # SARIMAX
    ts_train = train_df.set_index(date_col)[target_col]

    p = st.number_input("AR (p):", 0, 5, 1)
    d = st.number_input("Diferenciación (d):", 0, 2, 1)
    q = st.number_input("MA (q):", 0, 5, 1)

    try:
        sarimax_model = SARIMAX(ts_train, order=(p, d, q))
        sarimax_fit = sarimax_model.fit(disp=False)
        sarimax_forecast = sarimax_fit.get_forecast(steps=len(test_df))
        sarimax_pred = sarimax_forecast.predicted_mean
    except Exception as e:
        st.error(f"Error al ajustar SARIMAX: {e}")
        return

    # Datos reales de test
    y_true = test_df[target_col].values

    # Predicciones Prophet alineadas con test
    y_pred_prophet = prophet_forecast["yhat"].values

    # Predicciones SARIMAX alineadas
    y_pred_sarimax = sarimax_pred.values

    # Métricas
    def calculate_metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        return mae, rmse, mape

    prophet_mae, prophet_rmse, prophet_mape = calculate_metrics(y_true, y_pred_prophet)
    sarimax_mae, sarimax_rmse, sarimax_mape = calculate_metrics(y_true, y_pred_sarimax)

    st.markdown("### 📊 Comparación de métricas en conjunto de prueba")
    st.table(pd.DataFrame({
        "Modelo": ["Prophet", "SARIMAX"],
        "MAE": [prophet_mae, sarimax_mae],
        "RMSE": [prophet_rmse, sarimax_rmse],
        "MAPE (%)": [prophet_mape, sarimax_mape]
    }))

    # Gráfico comparativo
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(test_df[date_col], y_true, label="Real", color="black")
    ax.plot(test_df[date_col], y_pred_prophet, label="Prophet", color="blue")
    ax.plot(test_df[date_col], y_pred_sarimax, label="SARIMAX", color="red")
    ax.legend()
    ax.set_title("📈 Comparación de Predicciones en el Conjunto de Prueba")
    st.pyplot(fig)

    # Mejor modelo
    best_model = "Prophet" if prophet_rmse < sarimax_rmse else "SARIMAX"
    st.success(f"✅ **Mejor modelo según RMSE:** {best_model}")

    # Pronóstico futuro
    future_periods = st.slider("¿Cuántos períodos futuros deseas predecir?", 1, 365, 30)
    if st.button("🔮 Generar pronóstico futuro con el mejor modelo"):
        if best_model == "Prophet":
            future_df = prophet_model.make_future_dataframe(periods=future_periods)
            forecast = prophet_model.predict(future_df)
            fig_future = prophet_model.plot(forecast)
            st.pyplot(fig_future)
        else:
            ts_full = df.set_index(date_col)[target_col]
            final_model = SARIMAX(ts_full, order=(p, d, q)).fit(disp=False)
            future_forecast = final_model.get_forecast(steps=future_periods)
            future_pred = future_forecast.predicted_mean

            future_dates = pd.date_range(start=ts_full.index[-1], periods=future_periods+1, freq="D")[1:]
            fig_future, ax_future = plt.subplots()
            ts_full.plot(ax=ax_future, label="Histórico")
            future_pred.index = future_dates
            future_pred.plot(ax=ax_future, label="Pronóstico")
            ax_future.legend()
            st.pyplot(fig_future)

