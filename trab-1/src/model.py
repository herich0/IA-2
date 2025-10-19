import numpy as np

class MLP:
    def __init__(self, input_size, hidden_layers, output_size, learning_rate=0.01):
        self.lr = learning_rate
        self.weights = []
        self.biases = []
        self.activations = []
        
        layer_sizes = [input_size] + hidden_layers + [output_size]
        
        for i in range(len(layer_sizes) - 1):
            W = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(W)
            self.biases.append(b)

    def relu(self, Z):
        return np.maximum(0, Z)

    def relu_derivative(self, Z):
        return Z > 0

    def forward(self, X):
        self.activations = [X]
        A_prev = X
        
        for i in range(len(self.weights)):
            Z = np.dot(A_prev, self.weights[i]) + self.biases[i]
            if i < len(self.weights) - 1:
                A = self.relu(Z)
                self.activations.append(A)
                A_prev = A
            else:
                self.activations.append(Z)
                return Z

    def compute_loss(self, y_pred, y_true):
        return np.mean((y_pred - y_true) ** 2)

    def backward(self, X, y_pred, y_true):
        m = X.shape[0]
        
        dZ = (y_pred - y_true) / m
        
        for i in reversed(range(len(self.weights))):
            dW = np.dot(self.activations[i].T, dZ)
            db = np.sum(dZ, axis=0, keepdims=True)

            self.weights[i] -= self.lr * dW
            self.biases[i] -= self.lr * db

            if i > 0:
                dA = np.dot(dZ, self.weights[i].T)
                dZ = dA * self.relu_derivative(self.activations[i])

    def train(self, X, y, epochs=1000):
        losses = []
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = self.compute_loss(y_pred, y)
            losses.append(loss)
            self.backward(X, y_pred, y)
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
        return losses

    def predict(self, X):
        return self.forward(X)