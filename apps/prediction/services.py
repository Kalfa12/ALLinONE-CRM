"""Inference service for the Product Potential Categorizer."""
from functools import lru_cache
from pathlib import Path

from django.conf import settings


@lru_cache(maxsize=1)
def _bundle():
    """Load the trained model + column list once per process."""
    import joblib  # imported lazily to keep startup cheap

    path = Path(settings.ML_MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(
            f'Model not found at {path}. Run: python ml/train.py'
        )
    return joblib.load(path)


def predict_potential(features: dict) -> tuple[str, float]:
    """Return (class_label, confidence) for a single product."""
    import pandas as pd

    bundle = _bundle()
    X = pd.DataFrame([features])
    X = pd.get_dummies(X)
    X = X.reindex(columns=bundle['columns'], fill_value=0)

    proba = bundle['model'].predict_proba(X)[0]
    classes = bundle['model'].classes_
    idx = int(proba.argmax())
    return str(classes[idx]), float(proba[idx])
