# -*- coding: utf-8 -*-
"""Q1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mDPsL4xjI7DHDwQIbgztxX_LfjO8Az-9
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

dataset_ns = np.loadtxt('/content/dataset.txt', delimiter=' ')

def split_data(dataset, train_ratio=0.70):
    np.random.shuffle(dataset)  # Shuffle before splitting
    split_idx = int(len(dataset) * train_ratio)
    return dataset[:split_idx], dataset[split_idx:]

data1 = dataset_ns[:500]
data2 = dataset_ns[500:1000]
data3 = dataset_ns[1000:]

data1 = np.hstack((data1, np.ones((data1.shape[0], 1))))  # Adding Label 1
data2 = np.hstack((data2, np.full((data2.shape[0], 1), 2)))  # Adding  Label 2
data3 = np.hstack((data3, np.full((data3.shape[0], 1), 3)))  # Adding Label 3
print("Number of data points in class1, class2 and class3 are", len(data1),",",  len(data2), "and", len(data3), "respectively")
data3 = data3[:500] # take only 500 points to match dimension

train1, test1 = split_data(data1) # train test split for Class1 dataset
train2, test2 = split_data(data2) # train test split for Class2 dataset
train3, test3 = split_data(data3) # train test split for Class3 dataset

train_len = len(train1) # as we see that length of the training datasets for all the classes is same
test_len = len(test1) # as we see that length of the testing datasets for all the classes is same

print("After splitting Class1 dataset, number of training sample is ", len(train1), "and number of testing samples is", len(test1))
print("After splitting Class2 dataset, number of training sample is ", len(train2), "and number of testing samples is", len(test2))
print("After splitting Class1 dataset, number of training sample is ", len(train3), "and number of testing samples is", len(test3))

# Combine
X_train = np.vstack((train1[:, :2], train2[:, :2], train3[:, :2]))
y_train = np.hstack((train1[:, 2], train2[:, 2], train3[:, 2]))

# Plot each class separately
def plot_scatter(ax, data, cls, title):
    colors = {1: 'r', 2: 'g', 3: 'b'}
    labels = {1: 'Class 1', 2: 'Class 2', 3: 'Class 3'}

    class_data = data[data[:, -1] == cls]
    ax.scatter(class_data[:, 0], class_data[:, 1], color=colors[cls], label=labels[cls], alpha=0.7)

    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_title(title)
    ax.legend()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
plot_scatter(axes[0], train1, 1, 'Training Data for Class 1')
plot_scatter(axes[1], train2, 2, 'Training Data for Class 2')
plot_scatter(axes[2], train3, 3, 'Training Data for Class 3')

plt.tight_layout()
plt.show()

def plot_scatter_all(data, title):
    plt.figure(figsize=(8, 6))
    colors = {1: 'r', 2: 'g', 3: 'b'}
    labels = {1: 'Class 1', 2: 'Class 2', 3: 'Class 3'}

    for cls in [1, 2, 3]:
        class_data = data[data[:, -1] == cls]
        plt.scatter(class_data[:, 0], class_data[:, 1], color=colors[cls], label=labels[cls], alpha=0.7)

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.show()

# Combine all training datasets
train_dataset = np.vstack((train1, train2, train3))

# Plot all classes in a single figure
print("Non-Linearly separable training dataset visualization for all three classes")
plot_scatter_all(train_dataset, 'Training Data for All 3 Classes')

# Combine all test datasets
test_dataset = np.vstack((test1, test2, test3)) # Combine all testing datasets
print("Non-Linearly separable testing datasets visualization for all three classes")
plot_scatter_all(test_dataset, 'Testing Data sampels for all 3 classes')

# Sigmoid activation
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_derivative(x):
    return x * (1 - x)

class Perceptron:
    def __init__(self):
        self.weight1 = 0.0
        self.weight2 = 0.0
        self.bias = 0.0
        self.eta = 0.0
        self.avg_error = []

def Train(data, actual_label, perceptron):
    '''Perceptron Training with Backpropagation'''

    # Forward Propagation
    weighted_sum = perceptron.weight1 * data[0] + perceptron.weight2 * data[1] + perceptron.bias
    pred_label = sigmoid(weighted_sum)  # Output after activation

    # Compute Error
    error = actual_label - pred_label

    # Back Propagation
    delta = error * sigmoid_derivative(pred_label)  # Compute gradient

    perceptron.weight1 += perceptron.eta * delta * data[0]
    perceptron.weight2 += perceptron.eta * delta * data[1]
    perceptron.bias += perceptron.eta * delta

    return abs(error)

'''First Perceptron'''
perceptron1_2 = Perceptron()
perceptron1_2.weight1 = 0.2
perceptron1_2.weight2 = 0.4
perceptron1_2.bias = 0
perceptron1_2.eta = 0.005

epochs = 30
for epoch in range(epochs):
    error = 0
    for i in range(len(train1)):
        error += Train(train1[i], 1, perceptron1_2)
        error += Train(train2[i], 0, perceptron1_2)
    perceptron1_2.avg_error.append(error / (2 * len(train1)))

'''Second Perceptron'''
perceptron2_3 = Perceptron()
perceptron2_3.weight1 = 0.1
perceptron2_3.weight2 = 0.5
perceptron2_3.bias = 0
perceptron2_3.eta = 0.005

epochs = 10
for epoch in range(epochs):
    error = 0
    for i in range(len(train2)):
        error += Train(train2[i], 1, perceptron2_3)
        error += Train(train3[i], 0, perceptron2_3)
    perceptron2_3.avg_error.append(error / (2 * len(train2)))

'''Third Perceptron'''
perceptron3_1 = Perceptron()
perceptron3_1.weight1 = 0.09
perceptron3_1.weight2 = 0.1
perceptron3_1.bias = 0
perceptron3_1.eta = 0.0004

epochs = 15
for epoch in range(epochs):
    error = 0
    for i in range(len(train3)):
        error += Train(train3[i], 1, perceptron3_1)
        error += Train(train1[i], 0, perceptron3_1)
    perceptron3_1.avg_error.append(error / (2 * len(train3)))

# plot Avg error vs Epochs for all three perceptrons
def plot_avg_error(ax, perceptron, label):
    ax.plot(range(len(perceptron.avg_error)), perceptron.avg_error, marker='o', linestyle='-', label=label, markersize=1)
    ax.set_xlabel('Epochs')
    ax.set_ylabel('Training Error')
    ax.set_title(f'Average Training Error\n{label}')
    ax.legend()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

plot_avg_error(axes[0], perceptron1_2, "Perceptron1_2")
plot_avg_error(axes[1], perceptron2_3, "Perceptron2_3")
plot_avg_error(axes[2], perceptron3_1, "Perceptron3_1")

plt.tight_layout()
plt.show()

def plot_decision_boundary(ax, data, class_a, class_b, perceptron, title):
    colors = {1: 'r', 2: 'g', 3: 'b'}
    labels = {1: 'Class 1', 2: 'Class 2', 3: 'Class 3'}

    for cls in [class_a, class_b]:
        class_data = data[data[:, -1] == cls]
        ax.scatter(class_data[:, 0], class_data[:, 1], color=colors[cls], label=labels[cls], alpha=0.7)

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    x_vals = np.linspace(x_min, x_max, 100)
    w1, w2, b = perceptron.weight1, perceptron.weight2, perceptron.bias
    if w2 != 0:
        y_vals = - (w1 * x_vals + b) / w2
        ax.plot(x_vals, y_vals, color='black', linestyle='-', label='Decision Boundary')

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_title(title)
    ax.legend()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

plot_decision_boundary(axes[0], train_dataset, 1, 2, perceptron1_2, 'Class1 vs Class2 Decision Boundary')
plot_decision_boundary(axes[1], train_dataset, 2, 3, perceptron2_3, 'Class2 vs Class3 Decision Boundary')
plot_decision_boundary(axes[2], train_dataset, 3, 1, perceptron3_1, 'Class3 vs Class1 Decision Boundary')

plt.tight_layout()
plt.show()

def plot_combined_decision_boundary(X_train, y_train, perceptrons, title="Combined Decision Boundary"):
    x_min, x_max = X_train[:, 0].min() - 1, X_train[:, 0].max() + 1
    y_min, y_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))

    # Apply the sigmoid function for decision boundaries
    Z1 = np.array([1 if sigmoid(perceptrons[0].weight1 * x + perceptrons[0].weight2 * y + perceptrons[0].bias) >= 0.5 else 0 for x, y in zip(xx.ravel(), yy.ravel())])
    Z2 = np.array([1 if sigmoid(perceptrons[1].weight1 * x + perceptrons[1].weight2 * y + perceptrons[1].bias) >= 0.5 else 0 for x, y in zip(xx.ravel(), yy.ravel())])
    Z3 = np.array([1 if sigmoid(perceptrons[2].weight1 * x + perceptrons[2].weight2 * y + perceptrons[2].bias) >= 0.5 else 0 for x, y in zip(xx.ravel(), yy.ravel())])

    # Assign class labels based on the three perceptrons' outputs
    Z_combined = np.zeros_like(Z1)
    for i in range(len(Z_combined)):
        if Z1[i] == 1:
            Z_combined[i] = 1
        elif Z2[i] == 1:
            Z_combined[i] = 2
        else:
            Z_combined[i] = 3

    Z_combined = Z_combined.reshape(xx.shape)

    # Define colormaps
    cmap_background = ListedColormap(["red", "green", "blue"])
    cmap_points = ListedColormap(["darkred", "darkgreen", "darkblue"])

    # Plot decision boundary
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z_combined, alpha=0.3, cmap=cmap_background)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cmap_points, edgecolors='k', label='Training Data')

    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()

# Example call
plot_combined_decision_boundary(X_train, y_train, [perceptron1_2, perceptron2_3, perceptron3_1])

# Visualization of all the decision boundaries between all the classes
def plot_data_with_boundaries(data, title, perceptrons):
    plt.figure(figsize=(8, 6))

    colors = {1: 'r', 2: 'g', 3: 'b'}
    labels = {1: 'Class 1', 2: 'Class 2', 3: 'Class 3'}

    for cls in [1, 2, 3]:
        class_data = data[data[:, -1] == cls]
        plt.scatter(class_data[:, 0], class_data[:, 1], color=colors[cls], label=labels[cls], alpha=0.7)

    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()

    x_vals = np.linspace(x_min, x_max, 100)

    for perceptron, color in zip(perceptrons, ['black', 'purple', 'cyan']):
        w1, w2, b = perceptron.weight1, perceptron.weight2, perceptron.bias
        if w2 != 0:
            y_vals = - (w1 * x_vals + b) / w2
            plt.plot(x_vals, y_vals, color=color, linestyle='-')

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.show()

print('Sky blue line is separating Class1 and Class3 data points')
print('Black line is separating Class1 and Class2 data points')
print('Purple line is separating Class2 and Class3 data points')
plot_data_with_boundaries(train_dataset, 'Training Data with Decision Boundaries', [perceptron1_2, perceptron2_3, perceptron3_1])
print("Decision boundary on Training Data between each class made by it's respective perceptron for which they have trained")

class_votes_store = {}

def Test(test, i, actual_label):
    class_votes = [0, 0, 0]

    if sigmoid(perceptron1_2.weight1 * test[i][0] + perceptron1_2.weight2 * test[i][1] + perceptron1_2.bias) >= 0.5:
        class_votes[0] += 1
    else:
        class_votes[1] += 1

    if sigmoid(perceptron2_3.weight1 * test[i][0] + perceptron2_3.weight2 * test[i][1] + perceptron2_3.bias) >= 0.5:
        class_votes[1] += 1
    else:
        class_votes[2] += 1

    if sigmoid(perceptron3_1.weight1 * test[i][0] + perceptron3_1.weight2 * test[i][1] + perceptron3_1.bias) >= 0.5:
        class_votes[2] += 1
    else:
        class_votes[0] += 1

    class_votes_store[i] = (class_votes, actual_label)
    return class_votes

def check_prediction(class_votes, actual_label):
    predicted_label = class_votes.index(max(class_votes)) + 1
    return predicted_label != actual_label

y_true = []
y_pred = []

# Testing
misclassified = 0
test_len = len(test1)

for i in range(test_len):
    # Class 1
    true_label = 1
    class_votes = Test(test1, i, true_label)
    predicted_label = class_votes.index(max(class_votes)) + 1
    y_true.append(true_label)
    y_pred.append(predicted_label)
    misclassified += check_prediction(class_votes, true_label)
    # Class 2
    true_label = 2
    class_votes = Test(test2, i, true_label)
    predicted_label = class_votes.index(max(class_votes)) + 1
    y_true.append(true_label)
    y_pred.append(predicted_label)
    misclassified += check_prediction(class_votes, true_label)
    # Class 3
    true_label = 3
    class_votes = Test(test3, i, true_label)
    predicted_label = class_votes.index(max(class_votes)) + 1
    y_true.append(true_label)
    y_pred.append(predicted_label)
    misclassified += check_prediction(class_votes, true_label)

correctly_classified = len(y_true) - misclassified
wrongly_classified = misclassified
accuracy = (correctly_classified / (correctly_classified + wrongly_classified)) * 100

print("Total number of correctly classified samples:", correctly_classified)
print("Total number of misclassified samples:", wrongly_classified)
print("Classification Accuracy:", round(accuracy, 2), "%")
conf_matrix = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=[1, 2, 3], yticklabels=[1, 2, 3])
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix")
plt.show()