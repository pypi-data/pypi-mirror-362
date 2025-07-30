from datetime import timedelta

import numpy as np
import pandas as pd

from ..utils import check_accelerometer_data, get_sampling_frequency


def get_mad(
    df: pd.DataFrame,
    epoch: int,
    *,
    sampling_frequency: float | None = None,
) -> pd.Series:
    # Get sampling frequency
    sampling_frequency = sampling_frequency or get_sampling_frequency(df)

    check_accelerometer_data(df)

    # Calculate vector magnitude and subtract 1g (gravity)
    vm = pd.Series(np.linalg.norm(df.values, axis=1), name='vm', index=df.index)
    del df

    # Calculate the epoch mean
    means = vm.resample(timedelta(seconds=epoch)).mean()
    means.name = 'epoch_mean'

    # Merge the vector magnitude with the epoch means on nearest index
    mad = pd.merge_asof(vm, means, left_index=True, right_index=True, direction='nearest')
    del vm, means

    # Calculate the mean absolute deviation
    mad['diff'] = np.abs(mad['vm'] - mad['epoch_mean'])
    mad = mad['diff'].resample(timedelta(seconds=epoch)).mean()
    mad.name = 'mad'

    return mad.astype('float32')
