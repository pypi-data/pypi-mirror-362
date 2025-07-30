from eradication_data_requirements.plot_cpue_series import (
    calculate_cpue_and_cumulative_by_flight,
    plot_cumulative_series_cpue,
)

import pandas as pd
import typer
import matplotlib.pyplot as plt

app = typer.Typer()


@app.command()
def version():
    pass


@app.command()
def plot_cumulative_series_cpue_by_flight(
    effort_capture_path: str = typer.Option("", help="Input file path"),
    output_png: str = typer.Option("", help="Output file path"),
    fontsize: int = typer.Option(27, help="Font size of axis"),
):
    effort_capture_df = pd.read_csv(effort_capture_path)
    data_year = calculate_cpue_and_cumulative_by_flight(effort_capture_df)
    plot_cumulative_series_cpue(fontsize, data_year)
    plt.savefig(output_png, dpi=300, transparent=True)
