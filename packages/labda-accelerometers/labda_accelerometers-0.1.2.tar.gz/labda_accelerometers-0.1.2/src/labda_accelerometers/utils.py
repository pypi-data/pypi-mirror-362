from datetime import time

import numpy as np
import pandas as pd

LOGGER = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {'labda_accelerometers': {'level': 'INFO', 'handlers': ['console'], 'propagate': False}},
    'root': {'level': 'WARNING', 'handlers': ['console']},
}


def get_sampling_frequency(
    df: pd.DataFrame | pd.Series,
    *,
    samples: int | None = 5_000,
) -> float:
    # Use subset of data for efficiency
    time_subset = df.index[:samples] if samples else df.index

    if len(time_subset) < 2:
        raise ValueError('DataFrame must have at least 2 samples to calculate sampling frequency.')

    # Convert to nanoseconds then to seconds for time differences
    time_diffs_seconds = np.diff(time_subset.astype('int64')) / 1e9

    # Calculate mean sampling interval and convert to frequency
    mean_interval = np.mean(time_diffs_seconds)

    if mean_interval <= 0:
        raise ValueError('Invalid time intervals detected in data.')

    return (1.0 / mean_interval).item()


def parse_time(time: str | time) -> time:
    if isinstance(time, str):
        return pd.to_datetime(time).time()

    return time


def check_accelerometer_data(df: pd.DataFrame) -> None:
    if df.shape[1] != 3:
        raise ValueError(
            f'DataFrame must have exactly 3 columns for accelerometer data, but has {df.shape[1]} columns.'
        )
