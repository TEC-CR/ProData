import numpy as np
from scipy.stats import t, ttest_1samp


def confidence_interval_mean(data, confidence=0.95):

    n = len(data)

    mean = np.mean(data)

    se = np.std(data, ddof=1) / np.sqrt(n)

    h = se * t.ppf(
        (1 + confidence) / 2,
        n - 1
    )

    return mean - h, mean + h


def one_sample_ttest(data, mu):

    stat, p = ttest_1samp(
        data,
        mu
    )

    return stat, p