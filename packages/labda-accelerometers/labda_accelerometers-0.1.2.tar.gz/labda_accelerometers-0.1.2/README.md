<div align="left">
  <a href="https://pypi.org/project/labda-accelerometers/">
    <img src="https://img.shields.io/pypi/v/labda-accelerometers" alt="PyPi Latest Release"/>
  </a>
  <a href="https://pypi.org/project/labda-accelerometers/">
    <img src="https://img.shields.io/pypi/pyversions/labda-accelerometers.svg" alt="Python Versions"/>
  </a>
  <a href="https://pepy.tech/projects/labda-accelerometers">
    <img src="https://static.pepy.tech/badge/labda-accelerometers/month" alt="Monthly Downloads"/>
  </a>
  <a href="#">
    <img src="#" alt="DOI Latest Release"/>
  </a>
  <a href="https://github.com/josefheidler/labda-accelerometers/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/labda-accelerometers/labda-accelerometers.svg" alt="License"/>
  </a>
</div>

# LABDA Accelerometers

A package designed to process data from movement sensors – accelerometers.

- Auto-calibration
- Non-wear detection
- Metrics: Counts, ENMO
- Python

See [documentation](#) for more details.

## Installation

Install using `pip install labda-accelerometers`.

## A Simple Example
```python
import pandas as pd
from labda_accelerometers import Metrics, AutoCalibrate, WearDetection

df = AutoCalibrate().calibrate(df)
print(df)
#>                                         acc_x     acc_y     acc_z
#> datetime  
#> 2021-09-09 00:00:07.009999990+02:00 -0.099318 -0.128671  0.995101
#> 2021-09-09 00:00:07.019999981+02:00  0.076385 -0.267248  0.995101
#> 2021-09-09 00:00:07.029999971+02:00  0.092358 -0.267248  0.927356

epoch = 1 # In seconds

acc_wear = WearDetection(epoch=epoch).from_acceleration(df)
metrics = Metrics(epoch=epoch)

enmo = metrics.enmo(df)
counts = metrics.counts(df)

results = pd.concat([acc_wear, enmo, counts], axis=1)
print(results)
#>                             wear      enmo  counts_x  counts_y  counts_z  counts_vm
#> datetime  
#> 2021-09-09 00:00:07+02:00  False  0.022882         0         5        51  51.244511  
#> 2021-09-09 00:00:08+02:00  False  0.024908         0         0         6   6.000000  
#> 2021-09-09 00:00:09+02:00  False  0.014403         0         0         0   0.000000  
```

Detailed information on labda-accelerometers processing and features is available [here](#).
