import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

# Funções auxiliares do seu projeto
def load_wine_data(path="data/winequality-red.csv", test_size=0.2, random_state=42):
    df = pd.read_csv(path, sep=';')
    X = df.drop('quality', axis=1).values
    y = df['quality'].values.reshape(-1, 1)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test, scaler

def approximate_accuracy(y_true, y_pred, tolerance=0.5):
    correct_predictions = np.abs(y_pred - y_true) <= tolerance
    accuracy = np.mean(correct_predictions) * 100
    return accuracy

def run_sklearn_experiment(dataset_name):
    print(f"--- Testando MLPRegressor do Scikit-Learn com o dataset {dataset_name} ---")
    
    # Carregar dados
    if dataset_name == "red":
        path = "data/winequality-red.csv"
    else:
        path = "data/winequality-white.csv"

    X_train, X_test, y_train, y_test, scaler = load_wine_data(path=path)

    # --- Criando o Modelo com Scikit-Learn ---
    # Parâmetros:
    # hidden_layer_sizes: define a arquitetura da rede
    # max_iter: número de épocas
    # learning_rate_init: taxa de aprendizado inicial
    print("\nTreinando modelo com Scikit-Learn (arquitetura=(16, 8))...")

    # O scikit-learn já usa ReLU e Adam por padrão.
    mlp_sklearn = MLPRegressor(hidden_layer_sizes=(16, 8),
                               max_iter=1000,
                               random_state=42,
                               learning_rate_init=0.01)

    # Treinando o modelo
    mlp_sklearn.fit(X_train, y_train.ravel()) # Usamos .ravel() para a saida y

    # Fazendo a previsao
    y_pred = mlp_sklearn.predict(X_test)

    # Calculando as métricas
    final_mse = mean_squared_error(y_test, y_pred)
    final_accuracy = approximate_accuracy(y_test, y_pred)

    print(f"\n >> MSE Final no Conjunto de Teste (Scikit-Learn): {final_mse:.4f} <<")
    print(f" >> Precisão Aproximada (tolerância de +/- 0.5): {final_accuracy:.2f}% <<")

if __name__ == "__main__":
    run_sklearn_experiment("red")
    run_sklearn_experiment("white")