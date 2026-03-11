import pandas as pd
import json
import os
from dataclasses import asdict

from pipeline.build_dataset import build_combined_rows

def save_dataset(path, rows, metadata):
    """
    Save a dataset to a parquet file and metadata to a companion json file.
    """
    df = pd.DataFrame(rows)
    df.to_parquet(path)
    with open(path.replace(".parquet", ".json"), "w") as f:
        json.dump(metadata, f)

def load_dataset(path):
    """
    Load a dataset from a parquet file and metadata from a companion json file.
    """
    df = pd.read_parquet(path)
    records = df.to_dict(orient="records")
    with open(path.replace(".parquet", ".json"), "r") as f:
        metadata = json.load(f)
    return records, metadata

def get_or_build_dataset(sp, path, limit=50, refresh=False):
    """
    Load a cached dataset if it exists, otherwise build it, save it, and return it.

    Returns:
        records, metadata
    """
    if os.path.exists(path) and not refresh:
        return load_dataset(path)

    rows = build_combined_rows(sp, limit=limit)

    metadata = {
        "pulled_at": rows[0].pulled_at if rows else None,
        "limit": limit,
        "num_rows": len(rows),
        "schema_version": 1,
        "time_ranges": ["short_term", "medium_term", "long_term"],
    }

    save_dataset(path, rows, metadata)

    records = [asdict(row) for row in rows]
    return records, metadata