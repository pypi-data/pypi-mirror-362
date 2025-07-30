from geci_plots import roundup, order_magnitude
import numpy as np
import matplotlib.pyplot as plt


def plot_cumulative_series_cpue(fontsize, cpue_df):
    seasons = cpue_df.index.values
    seasons_labels = [*seasons, ""]
    ticks_positions = np.arange(seasons[0], seasons[-1] + 2)
    ticks_positions[-1] = ticks_positions[-1] + 0.25

    _, ax = plt.subplots(1, 2, figsize=(23, 10), tight_layout=True)

    ax[0].plot(seasons, cpue_df["cpue"], "-o", linewidth=2)
    ax[0].set_xticks(ticks_positions)
    ax[0].set_xticklabels(seasons_labels, size=fontsize)
    ax[0].tick_params(axis="both", labelsize=fontsize)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["top"].set_visible(False)
    max_cpue = max(cpue_df["cpue"])
    cpue_limit = roundup(max_cpue, 10 ** order_magnitude(max_cpue))
    ax[0].set_ylim(0, cpue_limit)
    ax[0].set_ylabel("Catch Per Unit Effort (CPUE)", fontsize=fontsize)
    ax[0].set_xlim(ticks_positions[0] - 1, ticks_positions[-1])

    ax[1].plot(seasons, cpue_df["cumulative_cpue"], "-o", linewidth=2)
    ax[1].set_xticks(ticks_positions)
    ax[1].set_xticklabels(seasons_labels, size=fontsize)
    ax[1].tick_params(axis="both", labelsize=fontsize)
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["top"].set_visible(False)
    max_cum_cpue = max(cpue_df["cumulative_cpue"])
    cum_cpue_limit = roundup(max_cum_cpue, 10 ** order_magnitude(max_cum_cpue))
    ax[1].set_ylim(0, cum_cpue_limit)
    ax[1].set_ylabel("Cumulative CPUE", fontsize=fontsize)
    ax[1].set_xlim(ticks_positions[0] - 1, ticks_positions[-1])
    return ax


def calculate_cpue_and_cumulative_by_season(effort_capture_df):
    extract_year(effort_capture_df)
    effort_capture_df = effort_capture_df[effort_capture_df["Season"] >= 2014]
    column_name = "Season"
    return calculate_cpue_and_cumulative_by_column(effort_capture_df, column_name)


def calculate_cpue_and_cumulative_by_flight(effort_capture_df):
    column_name = "No_vuelo"
    return calculate_cpue_and_cumulative_by_column(effort_capture_df, column_name)


def calculate_cpue_and_cumulative_by_column(effort_capture_df, column_name):
    data_grouped_by_column = effort_capture_df.groupby(by=column_name).sum(numeric_only=False)
    data_grouped_by_column["cpue"] = (
        data_grouped_by_column["Capturas"] / data_grouped_by_column["Esfuerzo"]
    )
    data_grouped_by_column["cumulative_cpue"] = data_grouped_by_column["cpue"].cumsum()
    return data_grouped_by_column


def extract_year(effort_capture_df):
    effort_capture_df["Season"] = effort_capture_df["Fecha"].str[:4]
    effort_capture_df["Season"] = np.array([int(season) for season in effort_capture_df["Season"]])
