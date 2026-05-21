"""Trains the Product Potential Categorizer.

Run from the project root:

    python ml/train.py

It generates a synthetic dataset (if missing), fits a RandomForestClassifier
and dumps the trained model + column order to ml/model.pkl. Inference is
handled by apps/prediction/services.py.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

HERE = Path(__file__).resolve().parent
SEED_PATH = HERE / 'seed_data.csv'
MODEL_PATH = HERE / 'model.pkl'

CATEGORIES = ['beauty', 'fashion', 'tech', 'home', 'fitness', 'food']
COMPETITION = ['low', 'medium', 'high']
ANGLES = ['problem_solution', 'benefit', 'offer']


def generate_synthetic_dataset(n: int = 600, seed: int = 42) -> pd.DataFrame:
    """Toy data generator with non-trivial decision rules so the model has signal."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        cat = rng.choice(CATEGORIES)
        price = float(np.round(rng.uniform(5, 200), 2))
        comp = rng.choice(COMPETITION, p=[0.3, 0.5, 0.2])
        angle = rng.choice(ANGLES)
        ctr = float(np.clip(rng.normal(0.025, 0.015), 0.001, 0.15))

        # latent score → class
        score = 0.0
        score += {'low': 1.5, 'medium': 0.5, 'high': -1.0}[comp]
        score += {'problem_solution': 0.7, 'offer': 0.4, 'benefit': 0.0}[angle]
        score += {'beauty': 0.6, 'tech': 0.5, 'fitness': 0.4,
                  'fashion': 0.2, 'home': 0.1, 'food': -0.1}[cat]
        score += (ctr - 0.025) * 30
        score += -0.005 * (price - 30)  # very expensive items penalised
        score += rng.normal(0, 0.6)

        if score > 1.2:
            cls = 'High'
        elif score > -0.2:
            cls = 'Medium'
        else:
            cls = 'Low'
        rows.append({
            'category': cat, 'price': price, 'competition_level': comp,
            'angle_type': angle, 'initial_ctr': ctr, 'potential': cls,
        })
    return pd.DataFrame(rows)


def main():
    if not SEED_PATH.exists():
        print(f'Seed file not found, generating synthetic dataset → {SEED_PATH}')
        df = generate_synthetic_dataset()
        df.to_csv(SEED_PATH, index=False)
    else:
        df = pd.read_csv(SEED_PATH)

    print(f'Loaded {len(df)} rows.')
    print('Class distribution:\n', df['potential'].value_counts())

    y = df['potential']
    X = pd.get_dummies(df.drop(columns=['potential']))

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )
    clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    clf.fit(Xtr, ytr)

    print('\n== Classification report (test set) ==')
    print(classification_report(yte, clf.predict(Xte)))

    print('Confusion matrix:')
    print(confusion_matrix(yte, clf.predict(Xte), labels=clf.classes_))

    joblib.dump({'model': clf, 'columns': X.columns.tolist()}, MODEL_PATH)
    print(f'\nModel written to {MODEL_PATH}')


if __name__ == '__main__':
    main()
