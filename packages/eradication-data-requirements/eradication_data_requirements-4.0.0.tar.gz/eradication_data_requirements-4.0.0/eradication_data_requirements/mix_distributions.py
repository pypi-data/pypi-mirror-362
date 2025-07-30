from bootstrapping_tools import generate_latex_interval_string
from eradication_data_requirements.calculate_intersect import get_confidence_interval

import numpy as np


def combine_distributions_from_dict(pop_status_a, pop_status_b):
    capturas_totales = pop_status_a["capturas"] + pop_status_b["capturas"]
    mixed_distribution = concatenate_remanent_distributions(pop_status_a, pop_status_b)
    remanents_interval = get_confidence_interval(mixed_distribution)
    remanents_interval_string = generate_latex_interval_string(
        remanents_interval, deltas=False, decimals=0
    )
    return {
        "remanentes": remanents_interval_string,
        "capturas": capturas_totales,
        "remanentes_distribution": list(mixed_distribution),
    }


def concatenate_remanent_distributions(pop_status_a, pop_status_b):
    remanents_a = [n0 - pop_status_a["capturas"] for n0 in pop_status_a["distribution"]]
    remanents_b = [n0 - pop_status_b["capturas"] for n0 in pop_status_b["distribution"]]
    return np.concatenate((remanents_a, remanents_b))
