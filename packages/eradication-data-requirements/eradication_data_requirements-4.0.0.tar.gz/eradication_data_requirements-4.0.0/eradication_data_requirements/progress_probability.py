import numpy as np
import warnings

from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.resample_raw_data import resample_eradication_data


def get_progress_probability(raw_data, bootstrap_number, seed):
    slope_distribution = get_slopes_distribution(raw_data, bootstrap_number, seed)
    progress_probability = calculate_progress_probability(slope_distribution)
    return np.round(progress_probability, decimals=3)


def calculate_progress_probability(slopes_distribution):
    valid_slopes = [valid_slope for valid_slope in slopes_distribution if not np.isnan(valid_slope)]
    slopes_len = len(valid_slopes)
    is_in_progress = valid_slopes < np.zeros(slopes_len)
    return sum(is_in_progress) / slopes_len


def get_slopes_distribution(raw_data, bootstrap_number, seed):
    rng = np.random.default_rng(seed)
    slopes_distribution = [
        get_slope(resample_eradication_data(raw_data, rng)) for _ in range(bootstrap_number)
    ]
    if np.isnan(slopes_distribution).all():
        raise TypeError("Empty slopes distribution")
    return slopes_distribution


def get_slope(data):
    try:
        parameters = fit_ramsey_plot(data)
    except AssertionError as error:
        warnings.warn(error)
        parameters = [np.nan]
    return parameters[0]
