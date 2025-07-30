from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="pyblocks_data",
    version="1.0.5",  # ✅ nueva versión estable
    author="Ana María Maraboli Pavez",
    description="Interfaz visual para análisis de datos y Machine Learning en Streamlit",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "pandas",
        "numpy<2.1",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "prophet",
        "statsmodels",
        "sweetviz",
        "nltk",
        "sentence-transformers",
        "plotly",
        "joblib",
        "scipy",
        "wordcloud",
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "pyblocks_data=pyblocks_data:main",  # comando largo
            "pybs=pyblocks_data:main"            # ✅ alias corto
        ],
    },
    python_requires=">=3.10",
)






