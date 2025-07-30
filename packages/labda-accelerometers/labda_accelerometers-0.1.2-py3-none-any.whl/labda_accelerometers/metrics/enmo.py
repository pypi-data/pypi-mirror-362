from typing import Literal

import numpy as np
import pandas as pd

from ..utils import check_accelerometer_data


def get_enmo(
    df: pd.DataFrame,
    epoch: int,
    *,
    absolute: bool = False,
    trim: bool = True,
) -> pd.Series:
    name: Literal['enmo', 'enmoa'] = 'enmo'

    check_accelerometer_data(df)

    # Calculate vector magnitude and subtract 1g (gravity)
    time = df.index
    vm = np.linalg.norm(df.values, axis=1) - 1.0
    del df

    # Apply absolute if requested
    if absolute:
        vm = np.abs(vm)
        name = 'enmoa'

    # Apply trimming if requested
    vm = np.maximum(vm, 0.0) if trim else vm

    # Create series with proper index
    vm_series = pd.Series(vm, index=time, name=name, dtype=np.float32)

    # Resample to epoch
    epoch_td = pd.Timedelta(seconds=epoch)
    return vm_series.resample(epoch_td).mean()
