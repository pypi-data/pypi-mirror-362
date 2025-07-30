import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    confusion_matrix, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_curve, 
    auc
)

class RandomForest:
    def __init__(self, n_trees=20, max_depth=10, min_samples_split=2):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []
    
    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
            tree = DecisionTreeClassifier(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
            n_samples = X.shape[0]
            idxs = np.random.choice(n_samples, n_samples, replace=True)
            tree.fit(X[idxs], y[idxs])
            self.trees.append(tree)

    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(predictions, 0, 1)
        return np.array([Counter(pred).most_common(1)[0][0] for pred in tree_preds])
    
    def predict_proba(self, X):
        tree_probs = np.array([tree.predict_proba(X) for tree in self.trees])
        return np.mean(tree_probs, axis=0)

def evaluate(y_true, y_pred, model_name):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\n{model_name} Results:")
    print(f"Confusion Matrix:\n{cm}")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall: {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")
    print(f"Specificity: {tn/(tn+fp):.4f}")

def randomforest():
    data = datasets.load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=1234
    )

    rf_sklearn = RandomForestClassifier(n_estimators=20, random_state=1234)
    rf_sklearn.fit(X_train, y_train)

    rf_custom = RandomForest(n_trees=20)
    rf_custom.fit(X_train, y_train)

    pred_sklearn = rf_sklearn.predict(X_test)
    pred_custom = rf_custom.predict(X_test)
    prob_sklearn = rf_sklearn.predict_proba(X_test)[:, 1]

    evaluate(y_test, pred_sklearn, "Random Forest (sklearn)")
    evaluate(y_test, pred_custom, "Random Forest (custom)")

    fpr, tpr, _ = roc_curve(y_test, prob_sklearn)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='grey', linestyle='--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.show()

    print(f"ROC AUC: {roc_auc:.4f}\n")
