# pymfpatch

A modular, end-to-end pipeline for gap-filling EnergyPlus EPW weather files using high-resolution ERA reanalysis (or other reference series) and a hybrid GRU + XGBoost approach.  
It automatically parses, cleans, feature-engineers, imputes missing meteorological variables, and writes out a fully compliant EPW-ready for building simulations.

------------------------------------------------------------------------

## Features

-   **Dual-stage imputation**
    -   **GRU** for sequential, multi-output regression on variables with temporal patterns (temperature, humidity, wind, radiation...)
    -   **XGBoost** for the remaining scalar variables (visibility, ceiling height, albedo, precipitation...)\
-   **Flexible configuration** of
    -   which variables to impute with GRU vs XGB\
    -   model hyperparameters (learning rate, depth, batch size, early stopping, ...)\
-   **EnergyPlus EPW input/output** with native header preservation\
-   **Utility functions** for parsing, cleaning, feature-engineering and final EPW formatting

------------------------------------------------------------------------

## Installation

### 1. Editable install from local source
``` bash
# clone & install in editable mode
git clone https://your-repo.org/your-org/pymfpatch.git
cd pymfpatch
pip install -e .
```

### 2. Install from PyPI
``` bash
pip install pymfpatch
```

### 3. GPU enabling
For fastest training/inference, run on a CUDA-enabled GPU.
By default pip install pymfpatch will pull in the CPU-only torch wheel.
If you have Python 3.12 and a compatible GPU, for example, you can upgrade to the GPU build with:
``` bash
pip install torch==2.7.1+cu128 --index-url https://download.pytorch.org/whl/cu128
```

## Quickstart

``` python
from pymfpatch import WeatherImputer
# 1) Instantiate the imputer with your reference (ERA) and target station EPWs:
imputer = WeatherImputer(
    epw_reference_path = 'Data/ERA/marignane-era.epw',
    epw_station_path   = 'Data/MF/marignane-mf.epw',
)

# 2) Run the imputation pipeline:
imputer.process()

# 3) Write out a fully-imputed EPW:
imputer.write("marignane-imputed.epw")
```
