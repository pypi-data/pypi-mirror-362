🧩 PyBlocks.Data (Pybs)
PyBlocks.Data (Pybs) es una interfaz visual interactiva para análisis de datos, Machine Learning y series temporales construida con Streamlit.
Permite cargar datos, explorarlos, procesarlos, modelarlos y exportar resultados sin escribir código, pero manteniendo la potencia de Python.

🚀 Características principales
✅ Gestión completa del flujo de datos

Carga de archivos CSV

Manejo de valores nulos

Análisis estadístico básico e inferencial

Visualizaciones interactivas

EDA automático con Sweetviz

✅ Machine Learning integrado

Transformaciones y preprocesamiento

Ingeniería de variables

Reducción de dimensionalidad (PCA)

Modelado con Scikit-learn

Clustering

Comparación y evaluación de modelos

Detección avanzada de outliers y anomalías

✅ Series temporales

Descomposición estacional

Pronósticos con Prophet y SARIMAX

Comparación de modelos de predicción

✅ Análisis avanzado

NLP y análisis de texto

Análisis de correlaciones

Conciliación y comparación de bases de datos

✅ Extras

Chatbot analítico con LLM

Exportación del proyecto

Resumen automático del flujo

📦 Instalación
Asegúrate de tener Python 3.10+ instalado.

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar el paquete desde PyPI
pip install pyblocks-data
▶️ Uso
Una vez instalado, puedes ejecutarlo con cualquiera de estos comandos:

pyblocks_data   # comando completo
pybs            # ✅ alias corto
Esto abrirá automáticamente la interfaz en tu navegador:

Local URL: http://localhost:8501
📂 Estructura interna (para desarrolladores)

pyblocks_data/
│
├── app.py
├── lego_blocks/
│   ├── load_data.py
│   ├── basic_stats.py
│   ├── ...
│   └── chatbot_llm.py
│
├── utils/
│   └── helpers.py
└── README.md
🛠️ Tecnologías usadas
Streamlit

Pandas

Scikit-learn

Prophet / SARIMAX

Sweetviz

Plotly

Wordcloud

NLTK

OpenAI API

❤️ Autor
Desarrollado con cariño por Ana Maraboli y Señor G (ChatGPT)

✨ ¿Quieres contribuir?

Haz un fork

Crea una rama nueva

git checkout -b feature-nueva
Envía un Pull Request






