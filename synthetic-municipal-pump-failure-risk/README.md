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

Original synthetic data generated for this benchmark; no third-party dataset or external source was used. Intended dedication: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/), if accepted by the hosting platform's license selector.

