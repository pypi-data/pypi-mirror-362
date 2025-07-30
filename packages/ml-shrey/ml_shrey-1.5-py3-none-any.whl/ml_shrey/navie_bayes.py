import csv
import math
import random
import statistics

def calculate_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

def run_naive_bayes(file_path):
    dataset = []
    
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dataset.append([float(attr) for attr in row])

    dataset_size = len(dataset)
    print('Dataset size:', dataset_size)

    train_size = int(0.7 * dataset_size)

    X_train = []
    X_test = dataset.copy()
    training_indexes = random.sample(range(dataset_size), train_size)

    for i in training_indexes:
        X_train.append(dataset[i])
        X_test.remove(dataset[i])

    # Separate training data by class
    classes = {}
    for sample in X_train:
        label = int(sample[-1])
        if label not in classes:
            classes[label] = []
        classes[label].append(sample)

    # Calculate mean and stdev for each class
    summaries = {}
    for class_value, samples in classes.items():
        summary = [(statistics.mean(attr), statistics.stdev(attr)) for attr in zip(*samples)]
        del summary[-1]  # Remove class column stats
        summaries[class_value] = summary

    # Predict labels for test data
    predictions = []
    for sample in X_test:
        probabilities = {}
        for class_value, class_summary in summaries.items():
            probabilities[class_value] = 1
            for i, attr in enumerate(class_summary):
                probabilities[class_value] *= calculate_probability(sample[i], attr[0], attr[1])
        
        predicted_label = max(probabilities, key=probabilities.get)
        predictions.append(predicted_label)

    # Calculate accuracy
    correct = 0
    for i in range(len(X_test)):
        if X_test[i][-1] == predictions[i]:
            correct += 1

    accuracy = (correct / len(X_test)) * 100
    print(f"Accuracy: {accuracy:.2f}%")

def naive_bayes(*args, **kwargs):
    return run_naive_bayes(*args, **kwargs)
