import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, shapiro


def descriptive_stats(data):

    return {
        "n": len(data),
        "media": np.mean(data),
        "mediana": np.median(data),
        "desv_std": np.std(data, ddof=1),
        "varianza": np.var(data, ddof=1),
        "minimo": np.min(data),
        "maximo": np.max(data),
        "asimetria": skew(data),
        "curtosis": kurtosis(data)
    }


def histogram(data):

    fig, ax = plt.subplots()

    ax.hist(
        data,
        bins="auto",
        edgecolor="black"
    )

    ax.set_title("Histograma")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")

    return fig

def boxplot(data):

    fig, ax = plt.subplots()

    ax.boxplot(data)

    ax.set_title("Diagrama de Caja")

    return fig


from scipy.stats import shapiro


def shapiro_test(data):

    stat, p = shapiro(data)

    return stat, p