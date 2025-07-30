import logging
import warnings
from dataclasses import dataclass
from datetime import time
from typing import Any

import numpy as np
import pandas as pd
from skdh.preprocessing import AccelThresholdWearDetection

from ..utils import get_sampling_frequency, parse_time

logger = logging.getLogger(__name__)


@dataclass
class WearDetection:
    epoch: int | None = None
    sampling_frequency: float | None = None

    def days(
        self,
        series: pd.Series,
        start: str | time | None = None,
        end: str | time | None = None,
    ) -> pd.Series:
        if start:
            start = parse_time(start)
            series = series.loc[series.index.time >= start]  # type: ignore

        if end:
            end = parse_time(end)
            series = series.loc[series.index.time < end]  # type: ignore

        sampling_frequency = self.sampling_frequency or get_sampling_frequency(series)

        stats = series.groupby(pd.Grouper(freq='D', origin='start_day', sort=True)).apply(
            lambda x: x.sum() / sampling_frequency
        )
        stats = pd.to_timedelta(stats, unit='s')

        return stats

    def from_acceleration(
        self,
        df: pd.DataFrame,
        **kwargs: Any,
    ) -> pd.Series:
        # Get sampling frequency
        sampling_frequency = self.sampling_frequency or get_sampling_frequency(df)

        # Prepare data for calibration
        time = df.index
        accel = df[['acc_x', 'acc_y', 'acc_z']]
        del df

        # Initialize wear detector
        wear_detector = AccelThresholdWearDetection(**kwargs)

        # Perform wear detection with error handling
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            wear = wear_detector.predict(
                time=(time.astype(np.int64) // 10**9).values,
                accel=accel.values,
                fs=sampling_frequency,
            ).get('wear')

        if wear is None or len(wear) == 0:
            raise ValueError('No wear periods found. Ensure the accelerometer data is valid and contains wear periods.')

        # Create boolean mask more efficiently using vectorized operations
        wear_mask = np.zeros(len(accel), dtype=bool)

        for start_idx, end_idx in wear:
            wear_mask[start_idx:end_idx] = True

        # Create Series with proper index
        wear_series = pd.Series(wear_mask, index=time, name='wear', dtype=bool)

        # Resample to epochs if requested
        if self.epoch is not None:
            epoch_duration = pd.Timedelta(seconds=self.epoch)
            # Use max aggregation: if any sample in epoch is wear time, epoch is wear time
            wear_series = wear_series.resample(epoch_duration).max()

        return wear_series
