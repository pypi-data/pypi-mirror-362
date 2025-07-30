import numpy as np
from bootstrapping_tools import generate_latex_interval_string
from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.progress_probability import get_progress_probability
from eradication_data_requirements.resample_raw_data import resample_eradication_data


def get_population_status_dict(raw_data, bootstrap_number, seed):
    data_with_cpue = add_cpue(raw_data)
    intercepts_distribution = get_intercepts_distribution(data_with_cpue, bootstrap_number, seed)
    interval = get_confidence_interval(intercepts_distribution)
    n0_interval = generate_latex_interval_string(interval, deltas=False, decimals=0)

    captures = data_with_cpue.Capturas.sum()
    remanentes = interval - captures
    remanentes_interval = generate_latex_interval_string(remanentes, deltas=False, decimals=0)
    progress_probability = get_progress_probability(data_with_cpue, bootstrap_number, seed)
    json_content = {
        "n0": n0_interval,
        "remanentes": remanentes_interval,
        "capturas": int(captures),
        "progress_probability": progress_probability,
        "distribution": intercepts_distribution,
    }
    return json_content


def add_cpue(raw_data):
    raw_data["CPUE"] = raw_data.Capturas / raw_data.Esfuerzo
    return raw_data


def get_confidence_interval(distribution):
    interval = np.round(np.percentile(distribution, [2.5, 50, 97.5])).astype(int)
    return interval


def get_intercepts_distribution(raw_data, bootstrap_number, seed=None):
    rng = np.random.default_rng(seed)
    raw_distribution = []
    distribution_size = 0
    captures = raw_data.Capturas.sum()
    while distribution_size < bootstrap_number:
        intercept = calculate_x_intercept(resample_eradication_data(raw_data, rng))
        if intercept > captures:
            raw_distribution.append(intercept)
        distribution_size = len(raw_distribution)
    return raw_distribution


def calculate_x_intercept(data):
    parameters = fit_ramsey_plot(data)
    return -parameters[1] / parameters[0]
