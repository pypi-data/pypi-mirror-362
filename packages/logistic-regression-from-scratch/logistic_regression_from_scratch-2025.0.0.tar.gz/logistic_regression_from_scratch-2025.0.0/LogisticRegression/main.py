class LogisticRegression:
  def __init__(self):
    self.w = None
    self.b = None
    print('Logistic Regression')

  # Prediction -:
  def __prediction(self, w, x, b):
    z = np.dot(x, w) + b
    p = 1 / (1 + np.exp(-z))

    return p

  # Calculating the Cost -: (J -> Cost Function)
  def __costFunction(self, p, y):
    J = -np.mean(y * np.log(p.T) + (1 - y) * np.log(1 - p.T))

    return J

  # Gradient Descent -:
  def __sigmoid(self, w, x, b):
    z = np.dot(x, w) + b

    return 1.0 / (1.0 + np.exp(-z))

  def __grad_b(self, w, x, b, y):
    fx = self.__sigmoid(w, x, b)

    return np.mean((fx - y) * fx * (1 - fx))

  def __grad_w(self, w, x, b, y):
    fx = self.__sigmoid(w, x, b)

    return np.mean((fx - y) * fx * (1 - fx) * x)

  def __gradientDescent(self, p, y, w, x, b, eta):
    dw = self.__grad_w(w, x, b, y)
    db = self.__grad_b(w, x, b, y)
    w -= eta * dw
    b -= eta * db

    return w, b

  def fit(self, x, y):
    weights = np.random.randn(x.shape[1], 1)
    bias = np.random.randn(1)

    epochs = 10000
    learning_rate = 0.01

    for i in range(epochs):
      y_predicted = self.__prediction(weights, x, bias)
      cost = self.__costFunction(y_predicted, y)
      weights, bias = self.__gradientDescent(y_predicted, y, weights, x, bias, learning_rate)

    self.w = weights
    self.b = bias

  def predict(self, testX):
    y_predicted = self.__prediction(self.w, testX, self.b)

    return y_predicted

  def score(self, testX, testY):
    y_predicted = self.__prediction(self.w, testX, self.b)
    y_predicted_binary = np.where(y_predicted >= 0.5, 1, 0)
    accuracy = np.mean(y_predicted_binary == testY)

    return accuracy * 100