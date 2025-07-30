import streamlit as st
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def render():
    st.subheader("📊 Estadística Inferencial Completa")

    # Menú principal
    test_type = st.radio(
        "Selecciona el tipo de prueba:",
        [
            "Prueba de una media",
            "Prueba de dos medias",
            "Prueba de una proporción",
            "Prueba de dos proporciones"
        ]
    )

    # ---- PRUEBA DE UNA MEDIA ----
    if test_type == "Prueba de una media":
        st.markdown("### 📏 Prueba de hipótesis para una media")

        # Entrada de datos
        sample_mean = st.number_input("Media muestral (x̄):", value=50.0)
        pop_mean = st.number_input("Media hipotética (μ₀):", value=45.0)
        sample_std = st.number_input("Desviación estándar (s):", value=10.0)
        n = st.number_input("Tamaño de muestra (n):", min_value=1, value=30)
        alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05)

        # Selección del tipo de prueba
        test_side = st.radio("Tipo de prueba", ["Bilateral", "Unilateral (mayor)", "Unilateral (menor)"])

        # Decidir z o t según n
        use_z = st.checkbox("Usar Z-Test (si conoces σ poblacional)")

        if st.button("Calcular prueba"):
            se = sample_std / np.sqrt(n)
            test_stat = (sample_mean - pop_mean) / se

            if use_z:
                dist = stats.norm(0, 1)
            else:
                dist = stats.t(df=n-1)

            if test_side == "Bilateral":
                p_value = 2 * (1 - dist.cdf(abs(test_stat)))
                crit = dist.ppf(1 - alpha/2)
                reject = abs(test_stat) > crit
            elif test_side == "Unilateral (mayor)":
                p_value = 1 - dist.cdf(test_stat)
                crit = dist.ppf(1 - alpha)
                reject = test_stat > crit
            else:
                p_value = dist.cdf(test_stat)
                crit = dist.ppf(alpha)
                reject = test_stat < crit

            st.write(f"**Estadístico de prueba:** {test_stat:.4f}")
            st.write(f"**Valor crítico:** {crit:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.success("✅ Rechazamos H₀" if reject else "❌ No rechazamos H₀")

            # Visualización
            x = np.linspace(-4, 4, 500)
            y = dist.pdf(x)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(x, y, label="Distribución")
            ax.axvline(test_stat, color="red", linestyle="--", label="Estadístico")
            ax.axvline(crit, color="green", linestyle=":", label="Valor crítico")
            if test_side == "Bilateral":
                ax.axvline(-crit, color="green", linestyle=":")
            ax.legend()
            st.pyplot(fig)

    # ---- PRUEBA DE DOS MEDIAS ----
    elif test_type == "Prueba de dos medias":
        st.markdown("### 📏 Prueba de hipótesis para dos medias (muestras independientes)")

        mean1 = st.number_input("Media muestra 1:", value=50.0)
        mean2 = st.number_input("Media muestra 2:", value=47.0)
        std1 = st.number_input("Desviación estándar 1:", value=8.0)
        std2 = st.number_input("Desviación estándar 2:", value=7.5)
        n1 = st.number_input("Tamaño muestra 1:", min_value=1, value=30)
        n2 = st.number_input("Tamaño muestra 2:", min_value=1, value=35)
        alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05)

        test_side = st.radio("Tipo de prueba", ["Bilateral", "Unilateral (mayor)", "Unilateral (menor)"])

        if st.button("Calcular prueba dos medias"):
            se = np.sqrt((std1**2)/n1 + (std2**2)/n2)
            test_stat = (mean1 - mean2) / se
            df = min(n1-1, n2-1)
            dist = stats.t(df=df)

            if test_side == "Bilateral":
                p_value = 2 * (1 - dist.cdf(abs(test_stat)))
                crit = dist.ppf(1 - alpha/2)
                reject = abs(test_stat) > crit
            elif test_side == "Unilateral (mayor)":
                p_value = 1 - dist.cdf(test_stat)
                crit = dist.ppf(1 - alpha)
                reject = test_stat > crit
            else:
                p_value = dist.cdf(test_stat)
                crit = dist.ppf(alpha)
                reject = test_stat < crit

            st.write(f"**Estadístico t:** {test_stat:.4f}")
            st.write(f"**Valor crítico:** {crit:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.success("✅ Rechazamos H₀" if reject else "❌ No rechazamos H₀")

    # ---- PRUEBA DE UNA PROPORCIÓN ----
    elif test_type == "Prueba de una proporción":
        st.markdown("### 📊 Prueba de hipótesis para una proporción")

        p_hat = st.number_input("Proporción muestral (p̂):", value=0.55)
        p0 = st.number_input("Proporción hipotética (p₀):", value=0.50)
        n = st.number_input("Tamaño de muestra:", min_value=1, value=100)
        alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05)

        test_side = st.radio("Tipo de prueba", ["Bilateral", "Unilateral (mayor)", "Unilateral (menor)"])

        if st.button("Calcular prueba proporción"):
            se = np.sqrt((p0*(1-p0))/n)
            test_stat = (p_hat - p0) / se
            dist = stats.norm(0, 1)

            if test_side == "Bilateral":
                p_value = 2 * (1 - dist.cdf(abs(test_stat)))
                crit = dist.ppf(1 - alpha/2)
                reject = abs(test_stat) > crit
            elif test_side == "Unilateral (mayor)":
                p_value = 1 - dist.cdf(test_stat)
                crit = dist.ppf(1 - alpha)
                reject = test_stat > crit
            else:
                p_value = dist.cdf(test_stat)
                crit = dist.ppf(alpha)
                reject = test_stat < crit

            st.write(f"**Estadístico Z:** {test_stat:.4f}")
            st.write(f"**Valor crítico:** {crit:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.success("✅ Rechazamos H₀" if reject else "❌ No rechazamos H₀")

    # ---- PRUEBA DE DOS PROPORCIONES ----
    elif test_type == "Prueba de dos proporciones":
        st.markdown("### 📊 Prueba de hipótesis para dos proporciones")

        p1 = st.number_input("Proporción muestra 1:", value=0.55)
        p2 = st.number_input("Proporción muestra 2:", value=0.48)
        n1 = st.number_input("Tamaño muestra 1:", min_value=1, value=100)
        n2 = st.number_input("Tamaño muestra 2:", min_value=1, value=120)
        alpha = st.slider("Nivel de significancia (α):", 0.01, 0.10, 0.05)

        test_side = st.radio("Tipo de prueba", ["Bilateral", "Unilateral (mayor)", "Unilateral (menor)"])

        if st.button("Calcular prueba dos proporciones"):
            p_pool = (p1*n1 + p2*n2) / (n1+n2)
            se = np.sqrt(p_pool*(1-p_pool)*(1/n1 + 1/n2))
            test_stat = (p1 - p2) / se
            dist = stats.norm(0, 1)

            if test_side == "Bilateral":
                p_value = 2 * (1 - dist.cdf(abs(test_stat)))
                crit = dist.ppf(1 - alpha/2)
                reject = abs(test_stat) > crit
            elif test_side == "Unilateral (mayor)":
                p_value = 1 - dist.cdf(test_stat)
                crit = dist.ppf(1 - alpha)
                reject = test_stat > crit
            else:
                p_value = dist.cdf(test_stat)
                crit = dist.ppf(alpha)
                reject = test_stat < crit

            st.write(f"**Estadístico Z:** {test_stat:.4f}")
            st.write(f"**Valor crítico:** {crit:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.success("✅ Rechazamos H₀" if reject else "❌ No rechazamos H₀")
