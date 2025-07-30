from dataclasses import dataclass

import pandas as pd

from .counts import get_counts
from .enmo import get_enmo
from .mad import get_mad


@dataclass
class Metrics:
    epoch: int

    def enmo(self, df: pd.DataFrame, absolute: bool = False, trim: bool = True) -> pd.Series:
        return get_enmo(df, epoch=self.epoch, absolute=absolute, trim=trim)

    def mad(self, df: pd.DataFrame, sampling_frequency: float | None = None) -> pd.Series:
        return get_mad(df, sampling_frequency=sampling_frequency, epoch=self.epoch)

    def counts(self, df: pd.DataFrame, sampling_frequency: float | None = None) -> pd.DataFrame:
        return get_counts(df, sampling_frequency=sampling_frequency, epoch=self.epoch)
