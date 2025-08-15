import warnings
warnings.filterwarnings("ignore")

import gzip
import os
import pickle
import pickletools

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from category_encoders.cat_boost import CatBoostEncoder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def save_model(filename: str, model: object):
    """
    Function saves model into pickle object.
    """
    file_path = os.path.join(BASE_DIR, "models", filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(f"Saving model to full path: {file_path}")
    with gzip.open(file_path, "wb") as f:
        pickled = pickle.dumps(model)
        optimized_pickle = pickletools.optimize(pickled)
        f.write(optimized_pickle)


def main():
    file_path = os.path.join(BASE_DIR, "data", "processed", "dm_office_sales.csv")
    df = pd.read_csv(file_path)

    features = ['training level', 'work experience', 'salary', 'level of education', 'division']
    target = 'sales'

    X = df[features].drop(target, axis=1, errors='ignore')
    y = df[target].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric_features = ['training level', 'work experience', 'salary']
    categorical_features = ['level of education', 'division']

    numeric_transformer = Pipeline(
        steps=[("scale", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[("encode", CatBoostEncoder())]
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    lin_reg = LinearRegression()

    model = Pipeline(steps=[("preprocess", preprocess), ("linear_reg", lin_reg)])

    # Train model
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MAE (before save): {mae:.3f}")
    print(f"Test R2 Score (before save): {r2:.3f}")

    x = range(len(y_test))
    plt.scatter(x[:10], y_test[:10], color='blue', label='Actual')
    plt.scatter(x[:10], y_pred[:10], color='red', label='Predicted')
    plt.xlabel('Sample Index')
    plt.ylabel('Target Value')
    plt.title('Actual vs Predicted')
    plt.legend()
    plt.show()

    model_path = "dm_office_sales_linreg.pkl.gz"
    save_model(model_path, model)
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()