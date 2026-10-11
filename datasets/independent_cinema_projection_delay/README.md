# Independent Cinema Projection Readiness Delays

## Provenance
This is an original, fully synthetic dataset generated specifically for this benchmark. No external dataset, records, or real venue or person information was used. It represents simulated screening package and venue readiness conditions; it is not a record of observed cinema operations.

## Contents
- `cinema_projection_readiness_raw.csv`: 10,000 rows and 25 columns. One row represents a simulated screening. The binary target `start_delay_over_5m` indicates whether the simulated screening starts more than five minutes late; its positive rate is 17.87%.
- All values are populated. For unencrypted packages (`encrypted_content_flag=0`), `key_validity_margin_min` is `0.000` as a numeric not-applicable placeholder; interpret that field only when the encryption flag is `1`.
- The `checksum_warning_flag` positive rate is 7.28%, so the flag is not nearly constant.
- Discrete frame-rate standards are represented in `frame_rate_class` as `fps_24`, `fps_25`, `fps_30`, `fps_48`, or `fps_60`. Audio configurations are represented in `audio_configuration` as `channels_2`, `channels_6`, `channels_8`, `channels_12`, or `channels_16`. These are categorical options rather than continuous numeric measurements.
- Identifiers are synthetic. The file contains operational-style categorical and numeric features, a binary target, and no personal or sensitive records.

## License
The dataset is dedicated to the public domain under **CC0 1.0 Universal**. See the adjacent `LICENSE` file and the [CC0 1.0 legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode).

## Files
- [Download the raw CSV](https://raw.githubusercontent.com/25kejdiwalsa-pixel/customer-segmentation/main/datasets/independent_cinema_projection_delay/cinema_projection_readiness_raw.csv)
- [View the CC0 notice](LICENSE)
