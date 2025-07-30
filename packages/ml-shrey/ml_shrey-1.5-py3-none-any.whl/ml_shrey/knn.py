import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

def run_knn_iris(test_size=0.4, random_state=1, neighbors=1):
    iris = load_iris()
    x = iris.data
    y = iris.target

    print("Sample input data:\n", x[:5])
    print("Sample target values:\n", y[:5])

    # Split the dataset
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=test_size, random_state=random_state)

    print("\nTotal Dataset Shape:", iris.data.shape)
    print("Training set size:", len(xtrain))
    print("Test set size:", len(ytest))

    # Train KNN
    knn = KNeighborsClassifier(n_neighbors=neighbors)
    knn.fit(xtrain, ytrain)

    # Predict
    pred = knn.predict(xtest)

    # Accuracy
    accuracy = metrics.accuracy_score(ytest, pred)
    print("\nAccuracy:", accuracy * 100, "%")

    # Display predictions in label form
    ytestn = [iris.target_names[i] for i in ytest]
    predn = [iris.target_names[i] for i in pred]

    print("\n  Predicted    Actual")
    for i in range(len(pred)):
        print(f"{i:<3} {predn[i]:<10} {ytestn[i]:<10}")

def knn(*args, **kwargs):
    return run_knn_iris(*args, **kwargs)
