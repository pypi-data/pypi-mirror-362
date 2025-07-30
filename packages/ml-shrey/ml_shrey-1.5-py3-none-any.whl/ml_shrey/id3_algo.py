import pandas as pd
import math

class Node:
    def __init__(self, value="", leaf=False, pred="", children=None):
        self.value, self.leaf, self.pred = value, leaf, pred
        self.children = children or []

def entropy(df):
    counts = df["answer"].value_counts()
    return 0 if len(counts) == 1 else -sum((c / len(df)) * math.log2(c / len(df)) for c in counts)

def best_attr(df, attrs):
    return max(attrs, key=lambda a: entropy(df) - sum(
        (len(s) / len(df)) * entropy(s) for s in [df[df[a] == v] for v in df[a].unique()]))

def build_tree(df, attrs):
    if entropy(df) == 0:
        return Node(leaf=True, pred=df["answer"].iloc[0])
    attr = best_attr(df, attrs)
    node = Node(value=attr)
    for val in df[attr].unique():
        subset = df[df[attr] == val]
        child = Node(value=val)
        child.children = [build_tree(subset, [a for a in attrs if a != attr])]
        node.children.append(child)
    return node

def print_tree(node, depth=0):
    print("  " * depth + node.value + (" -> " + node.pred if node.leaf else ""))
    for child in node.children:
        print_tree(child, depth + 1)

def classify(node, example):
    if node.leaf:
        return node.pred
    for child in node.children:
        if child.value == example[node.value]:
            return classify(child.children[0], example)

def id3(file_path):
    data = pd.read_csv(file_path)
    features = [f for f in data.columns if f != "answer"]
    tree = build_tree(data, features)
    print("Decision Tree:")
    print_tree(tree)
    print("-" * 15)
    # Use the same test sample as the original code
    new = {"outlook": "sunny", "temperature": "hot", "humidity": "normal", "wind": "strong"}
    print(f"Prediction for {new}: {classify(tree, new)}")
