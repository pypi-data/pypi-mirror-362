import numpy as np
import pandas as pd


from eradication_data_requirements.progress_probability import get_progress_probability
from eradication_data_requirements.calculate_intersect import add_cpue
from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.resample_raw_data import (
    resample_valid_data,
    resample_valid_cumulative_data,
)


def fit_resampled_captures(datos, bootstrapping_number):
    resampled_data = resample_valid_data(datos, bootstrapping_number)
    ramsey_series = [set_up_ramsey_time_series(sample) for sample in resampled_data]
    fits = [fit_ramsey_plot(ramsey_serie) for ramsey_serie in ramsey_series]
    return fits


def add_probs_to_effort_capture_data(data_copy, bootstrapping_number, window_length):
    resized_data = data_copy[data_copy.Esfuerzo != 0]
    complete_months_data = fill_missing_months_with_effort_one_and_captures_zero(resized_data)
    data_with_cpue = add_cpue(complete_months_data)
    probs_status = calculate_resampled_probability_by_window(
        data_with_cpue, bootstrapping_number, window_length
    )
    data_with_cpue = paste_status_by_window(data_with_cpue, probs_status, "prob", window_length)
    return data_with_cpue[["Fecha", "Esfuerzo", "Capturas", "prob"]]


def fill_missing_months_with_effort_one_and_captures_zero(effort_and_capture_data):
    data_copy = effort_and_capture_data.copy()
    data_with_all_months = complete_missing_months_in_year(data_copy)
    return fill_empty_months_with_effort_one_and_captures_zero(data_with_all_months)


def complete_missing_months_in_year(incomplete_data):
    incomplete_data["Fecha"] = pd.to_datetime(incomplete_data["Fecha"], format="%Y-%m-%d")
    incomplete_data = incomplete_data.set_index("Fecha")
    initial_year = pd.offsets.YearBegin()
    one_day = pd.offsets.Day()
    date_index = pd.date_range(
        incomplete_data.index.min() + one_day - initial_year, incomplete_data.index.max(), freq="MS"
    )
    filled_months_df = incomplete_data.reindex(date_index, fill_value=np.nan)
    filled_months_df["Fecha"] = filled_months_df.index.strftime("%Y-%m-%d").astype(str)
    return filled_months_df


def fill_empty_months_with_effort_one_and_captures_zero(data_copy):
    data_copy["Esfuerzo"] = data_copy["Esfuerzo"].fillna(1)
    data_copy["Capturas"] = data_copy["Capturas"].fillna(0)
    return data_copy.reset_index()


def paste_status(data_copy, probs_status, column_name):
    window_length = 6
    df = paste_status_by_window(data_copy, probs_status, column_name, window_length)
    return df


def paste_status_by_window(data_copy, probs_status, column_name, window_length):
    df = add_empty_column(data_copy, column_name)
    number_of_empty_rows = window_length - 1
    assert len(df.loc[number_of_empty_rows:, column_name]) == len(
        probs_status
    ), "Different dimensions"
    df.loc[number_of_empty_rows:, column_name] = probs_status
    return df


def add_empty_column(data_copy, column_name):
    df_copy = data_copy.copy()
    df_copy.loc[:, column_name] = np.nan
    return df_copy


def set_up_ramsey_time_series(data):
    cumulative_captures = pd.DataFrame()
    cumulative_captures["Fecha"] = data.Fecha
    cumulative_captures["Cumulative_captures"] = data["Capturas"].cumsum()
    cumulative_captures["CPUE"] = data["Capturas"] / data["Esfuerzo"]
    return cumulative_captures[["Fecha", "CPUE", "Cumulative_captures"]]


def fit_resampled_cumulative(datos, bootstrapping_number):
    ramsey_series = set_up_ramsey_time_series(datos)
    resampled_data = resample_valid_cumulative_data(ramsey_series, bootstrapping_number)
    fits = [fit_ramsey_plot(sample) for sample in resampled_data]
    return fits


def calculate_resampled_probability_by_window(ramsey_series, bootstrapping_number, window_length):
    seed = 42
    return [
        get_progress_probability(
            ramsey_series.iloc[(i - window_length) : i], bootstrapping_number, seed
        )
        for i in range(window_length, len(ramsey_series) + 1)
    ]


def calculate_six_months_slope(data):
    window_length = 6
    return [
        fit_ramsey_plot(data.iloc[(i - window_length) : i])
        for i in range(window_length, len(data) + 1)
    ]


def extract_slopes(slopes_intercept_data):
    return [slope[0] for slope in slopes_intercept_data]


def extract_prob(slopes_intercept_data):
    slopes = [np.asarray(extract_slopes(sample)) for sample in slopes_intercept_data]
    return [np.mean(samples < 0) for samples in slopes]
