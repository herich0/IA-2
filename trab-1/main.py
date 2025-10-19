from src.data_loader import load_wine_data
from src.model import MLP
from src.utils import plot_loss, mean_squared_error, approximate_accuracy
import numpy as np

def run_experiment(dataset_name):
    print(f"--- Treinando MLP com o dataset {dataset_name} ---")
    
    # Carregar dados
    if dataset_name == "red":
        path = "data/winequality-red.csv"
    else:
        path = "data/winequality-white.csv"

    X_train, X_test, y_train, y_test, scaler = load_wine_data(path=path)
    
    # Criar modelo com múltiplas camadas ocultas
    # Para usar apenas uma camada oculta, a lista seria [32]
    hidden_layers_config = [50,25] 
    
    learning_rate = 0.01
    print(f"Taxa de aprendizado se'lecionada: {learning_rate:.6f}")
    
    model = MLP(
        input_size=X_train.shape[1], 
        hidden_layers=hidden_layers_config, 
        output_size=1, 
        learning_rate=learning_rate
    )

    # Treinar modelo
    losses = model.train(X_train, y_train, epochs=1000)

    # Avaliar no teste
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    accuracy = approximate_accuracy(y_test, y_pred, tolerance=0.5)
    print(f"MSE no teste: {mse:.4f}")
    print(f"Precisão aproximada (tolerância de +/- 0.5): {accuracy:.2f}%\n")

    # Plotar curva de loss
    plot_loss(losses, save_path=f"results/loss_curve_{dataset_name}.png")

if __name__ == "__main__":
    run_experiment("red")
    run_experiment("white")