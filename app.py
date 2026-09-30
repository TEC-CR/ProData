import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("ProData - Análisis Estadístico y Confiabilidad")

st.write("Bienvenido a la versión web de ProData")
st.write("Escuela de Ingeniería en Producción Industrial, TEC")
st.write("ELemaitre 2026")

data = np.random.randn(100)
st.line_chart(data)


from utils.file_loader import load_file
from modules.descriptive import (
    boxplot,
    descriptive_stats,
    histogram,
    shapiro_test
)

from modules.inference import (
    confidence_interval_mean,
    one_sample_ttest
)

from modules.reliability import (
    fit_weibull,
    mttf,
    weibull_percentile,
    reliability_time
)

st.set_page_config(
    page_title="ProData",
    layout="wide"
)

st.title("📊 ProData")
st.subheader(
    "Análisis Estadístico y Confiabilidad"
)


menu = st.sidebar.selectbox(
    "Módulo",
    [
        "Estadística Descriptiva",
        "Inferencia",
        "Distribuciones",
        "Confiabilidad"
    ]
)
archivo = st.sidebar.file_uploader(
    "Seleccione un Archivo",
    type=["xlsx", "xls", "csv"]
)

if archivo:

    df = load_file(archivo)

    st.success("Archivo cargado correctamente")

    st.write(df.head())

    # ==================================================
    # ESTADÍSTICA DESCRIPTIVA
    # ==================================================

    if menu == "Estadística Descriptiva":

        st.header("Estadística Descriptiva")

        columna = st.selectbox(
            "Seleccione la Variable",
            df.columns,
            key="desc_var"
        )

        datos = df[columna].dropna()

        if st.button("Calcular estadísticas"):

            resultado = descriptive_stats(datos)

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Media",
                f"{resultado['media']:.3f}"
            )

            col2.metric(
                "Mediana",
                f"{resultado['mediana']:.3f}"
            )

            col3.metric(
                "Desv. Est.",
                f"{resultado['desv_std']:.3f}"
            )

            col4, col5, col6 = st.columns(3)

            col4.metric(
                "Mínimo",
                f"{resultado['minimo']:.3f}"
            )

            col5.metric(
                "Máximo",
                f"{resultado['maximo']:.3f}"
            )

            col6.metric(
                "n",
                resultado['n']
            )

            col7, col8 = st.columns(2)

            col7.metric(
                "Asimetría",
                f"{resultado['asimetria']:.3f}"
            )

            col8.metric(
                "Curtosis",
                f"{resultado['curtosis']:.3f}"
            )

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

    # ==================================================
    # INFERENCIA
    # ==================================================

    elif menu == "Inferencia":

        st.header("Inferencia Estadística")

        columna = st.selectbox(
            "Seleccione la variable",
            df.columns,
            key="col_inf"
        )

        datos = df[columna].dropna()

        st.subheader(
            "Intervalo de Confianza para la Media"
        )

        ic_inf, ic_sup = confidence_interval_mean(
            datos
        )

        st.write(
            f"IC 95%: [{ic_inf:.3f}, {ic_sup:.3f}]"
        )

        st.subheader(
            "Prueba t de una muestra"
        )

        mu = st.number_input(
            "Media hipotética (μ₀)",
            value=0.0
        )

        if st.button(
            "Ejecutar prueba t",
            key="ttest"
        ):

            stat, p = one_sample_ttest(
                datos,
                mu
            )

            st.write(
                f"Estadístico t = {stat:.4f}"
            )

            st.write(
                f"Valor p = {p:.4f}"
            )

            if p < 0.05:

                st.error(
                    "Se rechaza H₀"
                )

                st.write(
                    f"Existe evidencia estadística para afirmar que la media es diferente de {mu}."
                )

            else:

                st.success(
                    "No se rechaza H₀"
                )

                st.write(
                    f"No existe evidencia suficiente para afirmar que la media es diferente de {mu}."
                )

    # ==================================================
    # CONFIABILIDAD
    # ==================================================

    elif menu == "Confiabilidad":

        st.header("Análisis de Confiabilidad")

        columna = st.selectbox(
            "Seleccione la variable de tiempos",
            df.columns,
            key="conf_var"
        )

        datos = df[columna].dropna()

        beta, eta = fit_weibull(datos)

        st.subheader("Parámetros Weibull")

        col1, col2 = st.columns(2)

        col1.metric(
            "β (Forma)",
            f"{beta:.3f}"
        )

        col2.metric(
            "η (Escala)",
            f"{eta:.3f}"
        )

        b1 = weibull_percentile(0.01, beta, eta)
        b5 = weibull_percentile(0.05, beta, eta)
        b10 = weibull_percentile(0.10, beta, eta)
        b50 = weibull_percentile(0.50, beta, eta)
        b90 = weibull_percentile(0.90, beta, eta)

        valor_mttf = mttf(beta, eta)

        st.subheader("Indicadores de Confiabilidad")

        c1, c2, c3 = st.columns(3)

        c1.metric("B1", f"{b1:.2f}")
        c2.metric("B5", f"{b5:.2f}")
        c3.metric("B10", f"{b10:.2f}")

        c4, c5, c6 = st.columns(3)

        c4.metric("B50", f"{b50:.2f}")
        c5.metric("B90", f"{b90:.2f}")
        c6.metric("MTTF", f"{valor_mttf:.2f}")

        st.subheader("Calculadora de Percentiles")

        prob = st.slider(
            "Probabilidad (0-1)",
            min_value=0.01,
            max_value=0.99,
            value=0.90,
            step=0.01
        )

        percentil = weibull_percentile(
            prob,
            beta,
            eta
        )

        st.metric(
            f"B{prob*100:.0f}",
            f"{percentil:.2f}"
        )

        st.subheader("Calculadora de Confiabilidad")

        tiempo_eval = st.number_input(
            "Tiempo",
            min_value=0.0,
            value=100.0
        )

        R = reliability_time(
            tiempo_eval,
            beta,
            eta
        )

        st.metric(
            "R(t)",
            f"{R:.4f}"
        )

        t = np.linspace(
            0,
            datos.max() * 1.2,
            200
        )

        curva_R = np.exp(
            -(t / eta) ** beta
        )

        fig, ax = plt.subplots()

        ax.plot(
            t,
            curva_R,
            linewidth=2
        )

        ax.set_title("Curva de Confiabilidad Weibull")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("R(t)")

        st.pyplot(fig)



else:

    st.info(
        "Seleccione un archivo para comenzar."
    )
    