"""Create deterministic public/private challenge splits from the raw synthetic CSV.

The final 48 days are held out as private labels. Outputs are written under
prepared_dataset/ unless --output is supplied. Python standard library only.
"""
import argparse
import csv
from datetime import date, timedelta
from pathlib import Path

TARGET = "peak_demand_kw"
FIRST_DATE = date(2024, 1, 1)
TRAIN_DAYS = 192

def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=Path(__file__).with_name("peak_load_synthetic.csv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("prepared_dataset"))
    args = parser.parse_args()

    cutoff = FIRST_DATE + timedelta(days=TRAIN_DAYS)
    with args.raw.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        source_fields = reader.fieldnames
        if not source_fields or TARGET not in source_fields:
            raise ValueError(f"Raw CSV must contain {TARGET!r}")
        training, public_test, private_labels = [], [], []
        for row_id, row in enumerate(reader):
            record = {"id": row_id, **row}
            if date.fromisoformat(row["date"]) < cutoff:
                training.append(record)
            else:
                public_test.append({k: v for k, v in record.items() if k != TARGET})
                private_labels.append({"id": row_id, TARGET: row[TARGET]})

    if len(training) != 1536 or len(public_test) != 384:
        raise ValueError(f"Unexpected split sizes: train={len(training)}, test={len(public_test)}")

    public_dir = args.output / "public"
    private_dir = args.output / "private"
    train_fields = ["id", *source_fields]
    test_fields = ["id", *(field for field in source_fields if field != TARGET)]
    write_csv(public_dir / "train.csv", train_fields, training)
    write_csv(public_dir / "test.csv", test_fields, public_test)
    write_csv(public_dir / "sample_submission.csv", ["id", "prediction"],
              [{"id": row["id"], "prediction": "0.000"} for row in public_test])
    write_csv(private_dir / "test_labels.csv", ["id", TARGET], private_labels)
    print(f"Wrote 1,536 train rows and 384 held-out rows under {args.output}")

if __name__ == "__main__":
    main()

