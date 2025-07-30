from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="pyblocks_data",
    version="1.0.2",
    author="Ana María Maraboli Pavez",
    description="Interfaz visual para análisis de datos y Machine Learning en Streamlit",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "streamlit-option-menu",
        "pandas",
        "numpy>=1.23,<2.0",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "prophet",
        "statsmodels",
        "sweetviz",
        "nltk",
        "sentence-transformers"
    ],
    entry_points={
        "console_scripts": [
            # El comando de consola será pyblocks_data
            "pyblocks_data=pyblocks_data.cli:main"
        ],
    },
    python_requires=">=3.10",
)





