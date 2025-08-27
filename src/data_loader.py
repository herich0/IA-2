# src/data_loader.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_wine_data(path="data/winequality-red.csv", test_size=0.2, random_state=42):
    """Carrega e pré-processa o dataset de vinho."""
    df = pd.read_csv(path, sep=';')

    # Features e target
    X = df.drop('quality', axis=1).values
    y = df['quality'].values.reshape(-1, 1)

    # Normalização
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test, scaler
