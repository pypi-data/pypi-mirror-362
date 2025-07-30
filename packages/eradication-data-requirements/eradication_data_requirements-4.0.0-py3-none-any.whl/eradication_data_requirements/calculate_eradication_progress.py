from bootstrapping_tools import AbstractSeriesBootstrapper
from eradication_data_requirements.data_requirements_plot import fit_ramsey_plot
from eradication_data_requirements.resample_raw_data import resample_eradication_data

import numpy as np
import json


class ProgressBootstrapper(AbstractSeriesBootstrapper):
    def __init__(self, bootstrapper_parametrizer):
        bootstrapper_parametrizer.parameters["dataframe"]["CPUE"] = 1
        self.bootstrap_config = bootstrapper_parametrizer.parameters
        self.season_series = self.bootstrap_config["dataframe"]["Temporada"]
        self.data_series = self.add_cpue()
        self.parameters_distribution = self.get_parameters_distribution()

    def add_cpue(self):
        data = self.bootstrap_config["dataframe"]
        data["CPUE"] = data.Capturas / data.Esfuerzo
        return data

    def get_parameters_distribution(self):
        rng = np.random.default_rng(42)
        distribution = []
        distribution_size = 0
        captures = self.data_series.Capturas.sum()
        while self.bootstrap_config["N"] > distribution_size:
            sample = resample_eradication_data(self.data_series, rng)
            parameters = fit_ramsey_plot(sample)
            is_valid = -parameters[1] / parameters[0] > captures
            if is_valid:
                distribution.append((parameters[0], parameters[1]))
            distribution_size = len(distribution)
        return distribution

    def save_intervals(self, output_path):
        json_dict = self.get_parameters_dictionary()
        json_dict["slopes_latex_interval"] = json_dict.pop("main_parameter_latex_interval")
        with open(output_path, "w") as file:
            json.dump(json_dict, file)
