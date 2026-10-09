"""Generate a reproducible synthetic pump-maintenance dataset.

Run with Python 3 and NumPy/pandas installed. The script writes the raw CSV
beside itself and uses a fixed random seed so repeated runs are identical.
"""

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20261009
N_ROWS = 12_000
OUTPUT = Path(__file__).with_name("eris_pump_failure_raw.csv")


def main() -> None:
    rng = np.random.default_rng(SEED)

    zones = np.array(["Coastal", "Highland", "Industrial", "Inland", "Urban"])
    zone = rng.choice(zones, size=N_ROWS, p=[0.16, 0.13, 0.22, 0.27, 0.22])
    models = np.array(["centrifugal", "diaphragm", "submersible"])
    model = rng.choice(models, size=N_ROWS, p=[0.52, 0.18, 0.30])

    age = np.clip(rng.gamma(shape=2.3, scale=4.1, size=N_ROWS), 0.5, 25.0)
    runtime = np.clip(rng.normal(14.2, 4.0, size=N_ROWS), 1.0, 24.0)
    model_vibration = np.select(
        [model == "diaphragm", model == "submersible"], [0.35, -0.15], default=0.0
    )
    vibration = np.clip(
        rng.lognormal(mean=np.log(3.0), sigma=0.42, size=N_ROWS)
        + 0.035 * age
        + model_vibration,
        0.3,
        18.0,
    )
    rare_vibration = rng.random(N_ROWS) < 0.006
    vibration[rare_vibration] = rng.uniform(11.0, 16.0, rare_vibration.sum())

    model_heat = np.select(
        [model == "diaphragm", model == "submersible"], [2.5, -1.5], default=0.0
    )
    ambient_zone = np.select(
        [zone == "Coastal", zone == "Highland", zone == "Inland", zone == "Urban"],
        [2.0, -5.0, 1.0, 3.0],
        default=0.0,
    )
    ambient = np.clip(rng.normal(24.0, 8.0, N_ROWS) + ambient_zone, -5.0, 47.0)
    motor_temp = np.clip(
        39.0 + 0.78 * runtime + 0.72 * age + 0.65 * vibration + model_heat
        + 0.22 * (ambient - 24.0) + rng.normal(0.0, 5.5, N_ROWS),
        25.0,
        115.0,
    )
    rare_heat = rng.random(N_ROWS) < 0.003
    motor_temp[rare_heat] = np.clip(
        motor_temp[rare_heat] + rng.uniform(18.0, 32.0, rare_heat.sum()), 25.0, 125.0
    )

    pressure_model = np.select(
        [model == "diaphragm", model == "submersible"], [0.25, -0.35], default=0.0
    )
    discharge_pressure = np.clip(
        5.4 - 0.035 * age + pressure_model + rng.normal(0.0, 0.85, N_ROWS),
        1.0,
        10.0,
    )
    flow_rate = np.clip(
        25.0 - 0.48 * age - 0.45 * vibration + 1.1 * discharge_pressure
        + rng.normal(0.0, 3.2, N_ROWS),
        2.0,
        55.0,
    )
    starts_per_day = np.clip(
        rng.poisson(lam=np.select([model == "diaphragm"], [15.0], default=11.0)),
        0,
        60,
    )
    days_since_maintenance = rng.integers(0, 541, size=N_ROWS)
    prior_fault_rate = np.clip(0.12 + 0.028 * age + 0.035 * np.maximum(vibration - 3.0, 0), 0.05, 2.0)
    prior_faults = np.clip(rng.poisson(prior_fault_rate), 0, 8)

    zone_turbidity = np.select(
        [zone == "Coastal", zone == "Industrial", zone == "Highland"], [0.20, 0.30, -0.10], default=0.0
    )
    turbidity = np.clip(
        rng.lognormal(mean=np.log(5.0) + zone_turbidity, sigma=0.52, size=N_ROWS),
        0.1,
        60.0,
    )

    log_odds = (
        -3.25
        + 0.13 * (age - 8.0)
        + 0.58 * np.maximum(vibration - 4.0, 0.0)
        + 0.045 * np.maximum(motor_temp - 68.0, 0.0)
        + 0.004 * np.maximum(days_since_maintenance - 90.0, 0.0)
        + 0.52 * prior_faults
        + 0.02 * (runtime - 12.0)
        + 0.035 * (starts_per_day - 11.0)
        + 0.06 * (turbidity - 5.0)
        + 0.18 * (model == "diaphragm")
    )
    failure_probability = 1.0 / (1.0 + np.exp(-log_odds))
    failure_within_30d = rng.binomial(1, failure_probability)

    data = pd.DataFrame(
        {
            "record_id": [f"PMP-{i:06d}" for i in range(1, N_ROWS + 1)],
            "site_zone": zone,
            "pump_model": model,
            "pump_age_years": age,
            "daily_runtime_hours": runtime,
            "vibration_mm_s": vibration,
            "motor_temperature_c": motor_temp,
            "discharge_pressure_bar": discharge_pressure,
            "flow_rate_lps": flow_rate,
            "starts_per_day": starts_per_day,
            "days_since_maintenance": days_since_maintenance,
            "fault_events_past_12m": prior_faults,
            "water_turbidity_ntu": turbidity,
            "ambient_temperature_c": ambient,
            "failure_within_30d": failure_within_30d,
        }
    )

    # Sensor outages are somewhat more common at coastal and highland sites.
    remote_site = np.isin(zone, ["Coastal", "Highland"])
    missing_rates = {
        "daily_runtime_hours": (0.010, 0.010),
        "vibration_mm_s": (0.035, 0.025),
        "motor_temperature_c": (0.025, 0.020),
        "discharge_pressure_bar": (0.020, 0.015),
        "flow_rate_lps": (0.025, 0.015),
        "water_turbidity_ntu": (0.070, 0.050),
    }
    for column, (base_rate, remote_extra) in missing_rates.items():
        probability_missing = base_rate + remote_extra * remote_site
        data.loc[rng.random(N_ROWS) < probability_missing, column] = np.nan

    data.to_csv(OUTPUT, index=False, float_format="%.4f")
    rate = data["failure_within_30d"].mean()
    print(f"Wrote {len(data):,} rows to {OUTPUT}")
    print(f"Positive class: {rate:.2%}; seed: {SEED}")


if __name__ == "__main__":
    main()

