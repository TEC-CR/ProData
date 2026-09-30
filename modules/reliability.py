import numpy as np
from scipy.stats import weibull_min
from scipy.special import gamma


def fit_weibull(data):

    shape, loc, scale = weibull_min.fit(
        data,
        floc=0
    )

    return shape, scale


def mttf(beta, eta):

    return eta * gamma(
        1 + 1 / beta
    )


def weibull_percentile(
    probability,
    beta,
    eta
):

    return weibull_min.ppf(
        probability,
        beta,
        scale=eta
    )


def reliability_time(
    t,
    beta,
    eta
):

    return np.exp(
        -(t / eta) ** beta
    )