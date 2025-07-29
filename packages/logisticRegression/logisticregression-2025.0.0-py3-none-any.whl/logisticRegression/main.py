import numpy as np
import pandas as pd
  
class LogisticRegression : 

    def __init__(self , epochs = 1000, learningRate = 0.01):
        self.w = None
        self.b = None
        self.epochs = epochs
        self.learningRate = learningRate

    def pred(self, x):
        return 1.0 / (1.0 + np.exp(-((np.dot(self.w.T, x) + self.b))))

    def fit(self, x, y):
        m = x.shape[1]
        self.w = np.random.randn(n,1)
        self.b = np.random.randn(1)
        

        for i in range(self.epochs):
            p = self.pred(x)
            error = (p - y) * p * (1 - p)

            dw = (1 / m) * np.dot(x, error.T)
            db = (1 / m) * np.sum(error)

            self.w -= self.learningRate * dw
            self.b -= self.learningRate * db

            if i % 100 == 0:
                p = self.pred(x)
                J = -np.mean(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9))
                print(f"Epoch {i}, Loss: {J:.4f}")
            

    def predict(self ,x):
        y_predicted = self.pred(x)
        y_predicted = np.where(y_predicted >= 0.5, 1, 0)
        return y_predicted

    def accuracyScore(self,y,y_pred):
        accuracy = np.mean(y_pred == y)*100
        return accuracy

