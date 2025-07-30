import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def run_lwlr(file_path, tau=0.5):
    data = pd.read_csv(file_path)
    X_train = np.array(data['total_bill'])
    print(X_train)
    X_train = X_train[:, np.newaxis]
    print(len(X_train))
    y_train = np.array(data['tip'])
    X_test = np.array([i / 10 for i in range(500)])
    X_test = X_test[:, np.newaxis]
    y_test = []
    count = 0
    for r in range(len(X_test)):
        wts = np.exp(-np.sum((X_train - X_test[r]) ** 2, axis=1) / (2 * tau ** 2))
        W = np.diag(wts)
        factor1 = np.linalg.inv(X_train.T.dot(W).dot(X_train))
        parameters = factor1.dot(X_train.T).dot(W).dot(y_train)
        prediction = X_test[r].dot(parameters)
        y_test.append(prediction)
        count += 1
    print(len(y_test))
    y_test = np.array(y_test)
    plt.plot(X_train.squeeze(), y_train, 'o')
    plt.plot(X_test.squeeze(), y_test, 'o')
    plt.show()

def lwlr(*args, **kwargs):
    return run_lwlr(*args, **kwargs)
