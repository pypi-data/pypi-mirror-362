import streamlit as st
from streamlit_option_menu import option_menu

# ✅ IMPORTAMOS DESDE pyblocks_data.lego_blocks
from pyblocks_data.lego_blocks import (
    load_data, basic_stats, estadistica_inferencial, missing_values, visualizations, transformations,
    modeling, clustering, correlation_analysis, deteccion_avanzada, feature_engineering,
    pca_dimensionality, eda_sweetviz, nlp_analysis, series_temporales, pronostico, modelo_comparador,
    variable_selector, evaluacion_modelos, comparar_bases, conciliacion, export_project, chatbot_llm, project_summary
)

st.set_page_config(page_title="Modelo LEGO - Ciencia de Datos", layout="wide")
st.title("🧩 Interfaz Visual LEGO para Ciencia de Datos")

# ✅ Definimos categorías y sus bloques
categorias = {
    "📁 Datos": [
        "📁 Cargar Datos",
        "🧹 Manejo de Nulos",
        "📊 Estadísticas Básicas",
        "📊 Estadística Inferencial Completa",
        "📈 Visualizaciones",
        "📋 EDA Sweetviz",
        "🆚 Comparar Bases",
        "📑 Conciliación"
    ],
    "🤖 Machine Learning": [
        "🔄 Transformaciones",
        "🏗️ Ingeniería de Variables",
        "🧬 Reducción de Dimensionalidad",
        "🎯 Selección de Variables + Preprocesamiento",
        "🧠 Modelado",
        "📊 Comparador de Modelos",
        "🧪 Evaluación de Modelos",
        "🌐 Clustering",
        "🚨 Detección Avanzada de Outliers y Anomalías"
    ],
    "⏳ Series Temporales": [
        "⏳ Series Temporales",
        "📆 Pronóstico"
    ],
    "📜 Análisis Avanzado": [
        "📝 Análisis de Texto",
        "📌 Análisis de Correlación"
    ],
    "🛠️ Proyecto": [
        "🧾 Resumen del Proyecto",
        "🤖 Chatbot Analítico con LLM",
        "📤 Exportar Proyecto"
    ]
}

# ✅ Sidebar: Menú de Categorías
with st.sidebar:
    st.title("🧩 Flujo LEGO")

    categoria_seleccionada = option_menu(
        "📂 Categorías",
        list(categorias.keys()),
        icons=["folder", "cpu", "clock-history", "bar-chart", "tools"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"font-size": "20px"},
            "nav-link": {"font-size": "16px", "margin": "5px", "padding": "5px"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        }
    )

    # ✅ Segundo menú: Módulos de la categoría seleccionada
    bloque_seleccionado = option_menu(
        f"📦 Módulos en {categoria_seleccionada}",
        categorias[categoria_seleccionada],
        icons=["chevron-right"] * len(categorias[categoria_seleccionada]),
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#eef1f7"},
            "icon": {"font-size": "18px"},
            "nav-link": {"font-size": "15px", "margin": "4px"},
            "nav-link-selected": {"background-color": "#198754", "color": "white"},
        }
    )

# ✅ Función para renderizar cada módulo
def ejecutar_modulo(bloque):
    if bloque == "📁 Cargar Datos":
        load_data()
    elif bloque == "🧹 Manejo de Nulos":
        missing_values()
    elif bloque == "📊 Estadísticas Básicas":
        basic_stats()
    elif bloque == "📊 Estadística Inferencial Completa":
        estadistica_inferencial()
    elif bloque == "📈 Visualizaciones":
        visualizations()
    elif bloque == "📋 EDA Sweetviz":
        eda_sweetviz()
    elif bloque == "🆚 Comparar Bases":
        comparar_bases()
    elif bloque == "📑 Conciliación":
        conciliacion()
    elif bloque == "🔄 Transformaciones":
        transformations()
    elif bloque == "🏗️ Ingeniería de Variables":
        feature_engineering()
    elif bloque == "🧬 Reducción de Dimensionalidad":
        pca_dimensionality()
    elif bloque == "🎯 Selección de Variables + Preprocesamiento":
        variable_selector()
    elif bloque == "🧠 Modelado":
        modeling()
    elif bloque == "📊 Comparador de Modelos":
        modelo_comparador()
    elif bloque == "🧪 Evaluación de Modelos":
        evaluacion_modelos()
    elif bloque == "🌐 Clustering":
        clustering()
    elif bloque == "🚨 Detección Avanzada de Outliers y Anomalías":
        deteccion_avanzada()
    elif bloque == "⏳ Series Temporales":
        series_temporales()
    elif bloque == "📆 Pronóstico":
        pronostico()
    elif bloque == "📝 Análisis de Texto":
        nlp_analysis()
    elif bloque == "📌 Análisis de Correlación":
        correlation_analysis()
    elif bloque == "🧾 Resumen del Proyecto":
        project_summary()
    elif bloque == "🤖 Chatbot Analítico con LLM":
        chatbot_llm()
    elif bloque == "📤 Exportar Proyecto":
        export_project()

# ✅ Ejecutar el módulo elegido
ejecutar_modulo(bloque_seleccionado)



