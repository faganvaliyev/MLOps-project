import warnings
warnings.filterwarnings("ignore")

import gzip
import io
import os
import pickle
from typing import Iterable, Optional

import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_model(filepath: str):
    """
    Load a gzip-pickled model from disk.
    """
    with gzip.open(filepath, "rb") as f:
        p = pickle.Unpickler(f)
        model = p.load()
    return model


def _load_dataframe_from_bytes(
    file_content: bytes, filename: Optional[str]
) -> pd.DataFrame:
    """
    Read an uploaded file (bytes) into a DataFrame using file extension.
    Defaults to Excel if the extension is ambiguous.
    """
    name = (filename or "").lower()
    buffer = io.BytesIO(file_content)

    if name.endswith(".csv"):
        df = pd.read_csv(buffer)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        df = pd.read_excel(buffer, engine="openpyxl")
    else:
        df = pd.read_excel(buffer)
    return df


def main(
    file_content: Optional[bytes] = None, filename: Optional[str] = None
) -> Iterable:
    """
    Accepts raw file bytes and an optional filename to parse CSV/Excel,
    loads the trained model, and returns predictions.
    """
    if file_content:
        X_test = _load_dataframe_from_bytes(file_content, filename)
    else:
        X_test_path = os.path.join(BASE_DIR, "data", "external", "X_test.csv")
        X_test = pd.read_csv(X_test_path)

    model_path = os.path.join(BASE_DIR, "models", "dm_office_sales_linreg.pkl.gz")
    loaded_model = load_model(model_path)
    y_pred = loaded_model.predict(X_test)

    try:
        return y_pred.tolist()
    except TypeError:
        return [p for p in y_pred]


if __name__ == "__main__":
    preds = main()
    print(f"Generated {len(preds)} predictions")
    print(preds[:10])  
