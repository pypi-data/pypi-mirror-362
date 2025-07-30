import streamlit as st
import pandas as pd
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
nltk.download('stopwords')
from nltk.corpus import stopwords

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def render():
    st.subheader("💬 Análisis de Texto (NLP)")

    uploaded_file = st.file_uploader("Carga un archivo CSV con una columna de texto")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        column = st.selectbox("Selecciona la columna de texto", df.columns)

        # Limpieza de texto
        df["texto_limpio"] = df[column].astype(str).apply(clean_text)

        all_words = " ".join(df["texto_limpio"])
        stop_words = set(stopwords.words("spanish"))
        filtered_words = [word for word in all_words.split() if word not in stop_words]
        word_freq = Counter(filtered_words)

        st.markdown("### 🔠 Palabras más frecuentes")
        st.write(pd.DataFrame(word_freq.most_common(20), columns=["Palabra", "Frecuencia"]))

        # Word Cloud
        st.markdown("### ☁️ Nube de Palabras")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(filtered_words))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
