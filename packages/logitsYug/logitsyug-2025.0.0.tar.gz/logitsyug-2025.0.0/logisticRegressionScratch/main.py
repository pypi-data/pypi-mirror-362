class Regression:
   
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def computeLoss(Y, y_pred):
        epsilon = 1e-10
        return -np.mean(Y * np.log(y_pred + epsilon) + (1 - Y) * np.log(1 - y_pred + epsilon))

    def computeAccuracy(y_true, y_pred):
        y_pred_labels = (y_pred >= 0.5).astype(int)
        return np.mean(y_pred_labels == y_true) * 100

    def train(X, Y, learning_rate=0.1, epochs=100):
        m, n = X.shape  # m = samples, n = features
        W = np.zeros((n,))  # Dynamic weight initialization
        b = 0.0

        for epoch in range(epochs):
            Z = np.dot(X, W) + b
            y_pred = sigmoid(Z)
            loss = computeLoss(Y, y_pred)
            accuracy = computeAccuracy(Y, y_pred)

            dW = np.dot(X.T, (y_pred - Y)) / m
            db = np.sum(y_pred - Y) / m

            W -= learning_rate * dW
            b -= learning_rate * db

            if epoch % 10 == 0:
                print(f"Epoch {epoch:03d} | Loss: {loss:.4f} | Accuracy: {accuracy:.2f}%")

        return W, b  # Optional: return final parameters

    # Use any number of features — no hardcoding
    X = np.array([
        [1, 2, 3, 4, 5, 6],
        [6, 5, 4, 3, 2, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    Y = np.array([0, 1, 0])

    # Call training function
    train(X, Y)
