from bootstrapping_tools import resample_data, generate_latex_interval_string
from .calculate_intersect import get_confidence_interval


def get_monitoring_dict(raw_data, bootstrap_number):
    distribution = get_sum_distribution(raw_data, bootstrap_number)
    interval = get_confidence_interval(distribution)
    total_interval = generate_latex_interval_string(interval, deltas=False, decimals=0)
    return {"total": total_interval}


def get_sum_distribution(df, bootstrap_number):
    blocks_length = 1
    return [
        int(resample_data(df, seed, blocks_length).No_goats.sum())
        for seed in range(bootstrap_number)
    ]
