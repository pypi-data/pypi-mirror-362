import pandas as pd


def filter_data_by_method(raw_data, method):
    filtered_by_method = raw_data[raw_data.Tecnica == method]
    filtered_by_method.loc[:, ["Acumulado"]] = filtered_by_method.Capturas.cumsum()
    return filtered_by_method


def select_december_of_every_year(data):
    month_to_plot = "-12-"
    cutted_months = data[data.Fecha.str.contains(month_to_plot)]
    return pd.concat([cutted_months, data.iloc[-1:]])
