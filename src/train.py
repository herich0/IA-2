import numpy as np
from src.utils import mean_squared_error

def train_model(model, X_train, y_train, epochs=1000, lr=0.01):
    losses = []

    for epoch in range(epochs):
        # Forward
        y_pred = model.forward(X_train)
        
        # Cálculo do erro
        loss = mean_squared_error(y_train, y_pred)
        losses.append(loss)

        # Backpropagation
        grad_output = 2 * (y_pred - y_train) / y_train.shape[0]
        model.backward(X_train, grad_output, lr)

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    return losses
