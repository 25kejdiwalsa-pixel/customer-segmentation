# Cross-Neighborhood Microgrid Profile Discovery Under Temporal Drift

## Objective

Discover eight recurring neighborhood operating-profile families from synthetic microgrid observations. Use public feature rows and sparse labeled anchors to assign each test observation to its profile family. The task evaluates transfer to neighborhoods not represented in the public training rows.

## Data and split

The source file contains 24 anonymous neighborhoods observed over 240 chronological days. There are three independently perturbed neighborhoods in each of eight profile families. The source contains no profile label or district-type column.

The prepared public training set has 2,688 rows: two neighborhoods per profile family over training days 0–167. The test set has 576 rows: the final 72 days (indices 168–239) from the third, held-out neighborhood in each profile family. A test neighborhood does not appear in the public training rows. The split tests transfer across both neighborhoods and time.

`id` is a row key only. Do not use it as a model feature. The public feature files do not include neighborhood identifiers or profile labels.

## Labeled anchors

`public/anchors.csv` contains 24 labeled training rows: three per profile family. For each family, the anchors are from day 0 of its first training neighborhood, day 84 of its second training neighborhood, and day 167 of its first training neighborhood. Each anchor's `id` matches one row in `public/train.csv`; its label applies only to that row. Join anchors to training features by `id`. All other training rows and every test row are unlabeled.

Anchor labels are named `cluster_0` through `cluster_7`. The labels identify the profile families; ARI permits equivalent cluster-name permutations.

## Temporal shift and missing values

Later-period measurements include temporal changes, and observations include a small number of missing feature values. Fit imputation, scaling, and other preprocessing on public training data only. Do not use private labels or test outcomes.

## Submission

Submit `sample_submission.csv` with exactly two columns: `id,cluster`. Include every test `id` exactly once, with no extra rows, and assign one of the eight cluster labels to each row.

## Scoring

Submissions are scored using Adjusted Rand Index (ARI) against hidden test labels; higher is better. ARI compares pairwise cluster assignments while adjusting for chance and does not depend on the particular names assigned to clusters.

## Limitations

This is synthetic data generated for a benchmark and may not reflect real microgrid operations or support real-world conclusions. Neighborhoods are balanced by design; real sensor availability and neighborhood size may be imbalanced. Temporal changes are simulated and are not a substitute for validation on operational utility data.
