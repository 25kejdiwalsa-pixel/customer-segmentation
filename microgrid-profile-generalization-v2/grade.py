import pandas as pd
from sklearn.metrics import adjusted_rand_score


def _as_frame(value):
    if isinstance(value, pd.DataFrame):
        return value.copy()
    return pd.read_csv(value)


def grade(submission, answers):
    """Return ARI after validating and aligning rows by id."""
    try:
        pred = _as_frame(submission)
        truth = _as_frame(answers)

        required = {"id", "cluster"}
        if not required.issubset(pred.columns) or not required.issubset(truth.columns):
            return -1.0

        pred = pred[["id", "cluster"]].copy()
        truth = truth[["id", "cluster"]].copy()

        if pred["id"].isna().any() or truth["id"].isna().any():
            return -1.0
        if pred["id"].duplicated().any() or truth["id"].duplicated().any():
            return -1.0
        if pred["cluster"].isna().any() or truth["cluster"].isna().any():
            return -1.0

        pred["id"] = pred["id"].astype(str)
        truth["id"] = truth["id"].astype(str)
        pred["cluster"] = pred["cluster"].astype(str)
        truth["cluster"] = truth["cluster"].astype(str)

        if set(pred["id"]) != set(truth["id"]):
            return -1.0

        aligned = truth[["id"]].merge(
            pred, on="id", how="left", validate="one_to_one", sort=True
        )
        truth_sorted = truth.sort_values("id")["cluster"].to_numpy()
        pred_sorted = aligned["cluster"].to_numpy()

        score = float(adjusted_rand_score(truth_sorted, pred_sorted))
        if not (-1.0 <= score <= 1.0):
            return -1.0
        return score
    except Exception:
        # Malformed files receive the worst valid score rather than crashing.
        return -1.0
