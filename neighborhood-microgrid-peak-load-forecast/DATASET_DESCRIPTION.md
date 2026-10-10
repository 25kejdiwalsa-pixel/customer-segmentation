# Dataset Description

## Title

Neighborhood Microgrid Peak Load Forecast (NMPF-8x240)

## Overview

A new synthetic tabular dataset for estimating daily peak electricity demand across eight fictional neighborhood microgrids. It contains 1,920 observations: 240 consecutive days per zone, from 2024-01-01 through 2024-08-27. The regression target is `peak_demand_kw`, simulated same-day peak demand in kilowatts.

Demand is generated from weather, solar exposure, occupancy, EV charging, building characteristics, tariff plan, and community events, with nonlinear heat effects and small deterministic noise. The data is synthetic; no external source records are copied.

## Source URL

**Raw dataset URL:** [peak_load_synthetic.csv](https://raw.githubusercontent.com/25kejdiwalsa-pixel/customer-segmentation/main/neighborhood-microgrid-peak-load-forecast/peak_load_synthetic.csv)

**Data provenance:** Original synthetic data generated deterministically by the included [generate_dataset.py](https://raw.githubusercontent.com/25kejdiwalsa-pixel/customer-segmentation/main/neighborhood-microgrid-peak-load-forecast/generate_dataset.py) script; no third-party source records are used.

## File Structure

- `peak_load_synthetic.csv` — 1,920 labeled synthetic rows.
- `generate_dataset.py` — deterministic generator; uses only Python's standard library.

## Features

| Column | Type | Description |
|---|---|---|
| `zone_id` | string | Fictional microgrid identifier, Z01–Z08. |
| `district_type` | category | Neighborhood form associated with the zone. |
| `day_index` | integer | Zero-based day from the start of the synthetic period. |
| `date` | date | Date from 2024-01-01 through 2024-08-27. |
| `weekday` | integer | Day of week, Monday=0 through Sunday=6. |
| `month` | integer | Calendar month, 1–12. |
| `forecast_high_c` | float | Forecast daily high temperature in °C. |
| `forecast_low_c` | float | Forecast daily low temperature in °C. |
| `humidity_pct` | float | Forecast relative humidity percentage; some values are missing. |
| `solar_irradiance_kwh_m2` | float | Daily solar irradiation in kWh/m²; includes one deliberate high edge case. |
| `wind_kph` | float | Forecast wind speed in km/h; some values are missing. |
| `rain_mm` | float | Daily precipitation in mm; mostly zero with a deliberate heavy-rain edge case. |
| `occupancy_ratio` | float | Simulated fraction of typical neighborhood occupancy; some values are missing. |
| `ev_charge_share` | float | Simulated share of local load associated with EV charging. |
| `roof_albedo_pct` | integer | Fictional zone-level roof reflectivity percentage. |
| `tree_canopy_pct` | integer | Fictional zone-level tree canopy coverage percentage. |
| `cooling_system_age_yr` | integer | Fictional zone-level average cooling system age in years. |
| `tariff_plan` | category | Simulated plan: `flat`, `time_of_use`, or `critical_peak`. |
| `community_event` | integer | Simulated event flag, 0 or 1. |
| `peak_demand_kw` | float | **Target:** simulated daily peak electricity demand in kW. |

## Notes

- Rows are ordered by date and then zone; the same eight zones repeat. A time-based holdout is preferable to a random row split.
- Missingness is deliberate and deterministic in humidity, wind, and occupancy. The target is complete.
- The generator includes seasonal and day-to-day weather variation, nonlinear heat-related demand, zone effects, tariff/event effects, smooth noise, and controlled edge cases.
- This is a synthetic source file, not actual customer or utility consumption. A challenge package should split it deterministically and keep held-out target values private.
- This is synthetic data. Its raw CSV and generation scripts are hosted in this repository; no third-party records are included.



## License

No formal open license has been assigned to these files.

## Challenge Preparation

Run `python prepare_dataset.py` to create a deterministic time-based split:

- `prepared_dataset/public/train.csv` — 1,536 labeled rows from the first 192 days.
- `prepared_dataset/public/test.csv` — 384 unlabeled rows from the final 48 days.
- `prepared_dataset/public/sample_submission.csv` — expected `id,prediction` format.
- `prepared_dataset/private/test_labels.csv` — held-out labels for scoring.

The split uses dates, keeping all zones from a date together. The preparation script assigns stable row IDs and validates the expected split sizes.

