import streamlit as st
import numpy as np
import pandas as pd

st.title("ProData - Análisis Estadístico y Confiabilidad")

st.write("Bienvenido a la versión web de ProData")

data = np.random.randn(100)
st.line_chart(data)



from utils.file_loader import load_file
from modules.descriptive import (
    boxplot,
    descriptive_stats,
    histogram,
    shapiro_test
)

st.set_page_config(
    page_title="ProData",
    layout="wide"
)

st.title("📊 ProData")
st.subheader(
    "Análisis Estadístico y Confiabilidad"
)

archivo = st.file_uploader(
    "Seleccione un archivo",
    type=["xlsx", "xls", "csv"]
)

if archivo:

    df = load_file(archivo)

    st.success("Archivo cargado correctamente")

    st.write(df.head())

    columna = st.selectbox(
        "Seleccione la variable",
        df.columns
    )

    datos = df[columna].dropna()


if st.button("Calcular estadísticas"):

    resultado = descriptive_stats(datos)

    col1, col2, col3 = st.columns(3)

    col1.metric("Media", f"{resultado['media']:.3f}")
    col2.metric("Mediana", f"{resultado['mediana']:.3f}")
    col3.metric("Desv. Est.", f"{resultado['desv_std']:.3f}")

    col4, col5, col6 = st.columns(3)

    col4.metric("Mínimo", f"{resultado['minimo']:.3f}")
    col5.metric("Máximo", f"{resultado['maximo']:.3f}")
    col6.metric("n", resultado['n'])

    col7, col8 = st.columns(2)

    col7.metric("Asimetría", f"{resultado['asimetria']:.3f}")
    col8.metric("Curtosis", f"{resultado['curtosis']:.3f}")

    stat, p = shapiro_test(datos)

    st.metric(
        "Valor p (Shapiro-Wilk)",
        f"{p:.4f}"
    )

    if p > 0.05:
        st.success("No se rechaza normalidad")
    else:
        st.warning("Se rechaza normalidad")

    fig = histogram(datos)
    st.pyplot(fig)

    fig_box = boxplot(datos)
    st.pyplot(fig_box)



menu = st.sidebar.selectbox(
    "Módulo",
    [
        "Estadística Descriptiva",
        "Inferencia",
        "Distribuciones",
        "Confiabilidad"
    ]
)

