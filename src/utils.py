import numpy as np
import matplotlib.pyplot as plt

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred)**2)

def plot_loss(losses, save_path="results/loss_curve.png"):
    plt.figure()
    plt.plot(losses)
    plt.title("Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.savefig(save_path)
    plt.close()

def approximate_accuracy(y_true, y_pred, tolerance=0.5):
    """
    Calcula a precisão aproximada para um problema de regressão.
    Considera uma previsão como correta se a diferença absoluta for menor ou igual à tolerância.
    """
    correct_predictions = np.abs(y_pred - y_true) <= tolerance
    accuracy = np.mean(correct_predictions) * 100
    return accuracy
