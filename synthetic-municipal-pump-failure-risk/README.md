# Synthetic Municipal Pump Failure Risk

A fully synthetic tabular benchmark dataset for predicting whether a municipal water pump experiences a failure within 30 days.

## Contents

- `eris_pump_failure_raw.csv` — 12,000 synthetic inspection records with labels.
- `generate_dataset.py` — deterministic generator (NumPy/pandas; seed `20261009`).

## Target and size

- Target: `failure_within_30d` (`1` = simulated failure within 30 days; `0` = otherwise).
- 12,000 records; positive class rate is approximately 21.6%.
- `record_id` is a unique identifier and should not be used as a predictive feature.

## Data characteristics

The rows combine site and pump categories with age, operating readings, maintenance history, and turbidity. Sensor fields contain intentional missing values, with higher missingness at Coastal and Highland sites. Rare high vibration and temperature readings add edge cases. All values and labels are simulated; they do not represent real equipment or engineering safety limits.

## Reproduce

Run `python generate_dataset.py` with Python 3, NumPy, and pandas installed. The script writes the CSV beside itself. A fixed random seed makes repeated generation deterministic.

## License and source

Raw dataset source URL: [CSV](https://raw.githubusercontent.com/25kejdiwalsa-pixel/customer-segmentation/main/synthetic-municipal-pump-failure-risk/eris_pump_failure_raw.csv). Generator: [generate_dataset.py](https://github.com/25kejdiwalsa-pixel/customer-segmentation/blob/main/synthetic-municipal-pump-failure-risk/generate_dataset.py). The data is original and synthetic; no third-party dataset was used. The dataset and generator in this folder are dedicated under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/); see `LICENSE`.

