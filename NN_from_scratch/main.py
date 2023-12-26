import numpy as np
import pandas as pd
import os
import requests
import math
import warnings
from matplotlib import pyplot as plt


# scroll to the bottom to start coding your solution
warnings.filterwarnings('ignore')

def one_hot(data: np.ndarray) -> np.ndarray:
    y_train = np.zeros((data.size, data.max() + 1))
    rows = np.arange(data.size)
    y_train[rows, data] = 1
    return y_train


def plot(loss_history: list, accuracy_history: list, filename='plot'):

    # function to visualize learning process at stage 4

    n_epochs = len(loss_history)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Loss on train dataframe from epoch')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(accuracy_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Accuracy')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Accuracy on test dataframe from epoch')
    plt.grid()

    plt.savefig(f'{filename}.png')


# Task 1, define functions
def scale(X_train_input, X_test_input):
    return X_train_input / X_train_input.max(), X_test_input / X_test_input.max()

def xavier(n_in, n_out):
	return np.random.uniform(-(math.sqrt(6))/(math.sqrt(n_in + n_out)), (math.sqrt(6))/(math.sqrt(n_in + n_out)), (n_in, n_out))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def mse(array_pred, array_true):
    return np.mean((array_pred - array_true) ** 2)

def mse_derivative(array_pred, array_true):
    return 2 * (array_pred - array_true)

def sigmoid_derivative(function):
    return function * (1 - function)

# Task 2, define classes
class OneLayerNeural:
    def __init__(self, input_size, output_size):
        # Initiate weights and biases using Xavier
        self.input_size = input_size
        self.output_size = output_size
        # Initialize weights using Xavier initialization
        # self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / (input_size + output_size))
        # Initialize biases to zeros
        # self.biases = np.zeros((1, output_size))
        self.weights = xavier(input_size, output_size)
        self.biases = xavier(1, output_size)

        self.d_weights = None
        self.d_biases = None

    def forward(self, input_data):
        # Perform forward step
        self.input_data = input_data
        self.output = sigmoid(np.dot(input_data, self.weights) + self.biases)

        return self.output

    # def backprop(self, X, y, learning_rate):
    #     # Backpropagation to update weights and biases
    #     sigmoid_derivative_output = sigmoid_derivative(self.forward(X))
    #     # Compute gradients
    #     self.d_weights = np.dot(self.input_data.T, y * sigmoid_derivative_output)
    #     self.d_biases = np.sum(y * sigmoid_derivative_output, axis=0, keepdims=True)
    #
    #     # Update weights and biases
    #     self.weights -= learning_rate * self.d_weights
    #     self.biases -= learning_rate * self.d_biases
    #
    #     # Return gradient for the next layer in the network (if applicable)
    #     return np.dot(y * sigmoid_derivative_output, self.weights.T)

    def backprop(self, X, y, alpha):
        # Calculating gradients for each of
        # your weights and biases.
        # A(L) = sigmoid(w(L)*A(L-1)+b(L))
        dmse_step = mse_derivative(self.output, y)
        dsig_step = sigmoid_derivative(np.dot(X, self.weights) + self.biases)
        err = dmse_step * dsig_step
        d_weight = np.dot(X.T, err) / X.shape[0]
        d_bias = np.mean(err, axis=0)
        self.weights -= alpha * d_weight
        self.biases -= alpha * d_bias

def calculate_accuracy(model, input_data, target_data):
    # Forward pass to get predictions
    predictions = model.forward(input_data)
    # Convert one-hot encoded predictions to class indices
    predicted_classes = np.argmax(predictions, axis=1)

    # Convert one-hot encoded labels to class indices
    true_classes = np.argmax(target_data, axis=1)

    # Compare predicted classes with true classes
    correct_predictions = sum(1 for pred, true in zip(predicted_classes, true_classes) if pred == true)
    # print("correct_predictions  ", correct_predictions)

    # Calculate accuracy
    accuracy = correct_predictions / len(true_classes)

    return accuracy

def single_epoch_training(estimator, alpha, x_train_holder, y_train_holder, batch_size):
    num_batches = len(X_train_rescaled) // batch_size
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = (batch_num + 1) * batch_size

        # Extract a mini-batch for training
        mini_batch_X = x_train_holder[start_idx:end_idx, :]
        mini_batch_y = y_train_holder[start_idx:end_idx, :]
        estimator.forward(mini_batch_X)

        # Backpropagation step
        estimator.backprop(mini_batch_X, mini_batch_y, alpha)

        # Forward step again for the same two items

        # print(np.argmax(output_forward_after_backprop, axis=1))

        # Calculate Mean Squared Error (MSE) between the actual y_train and the predicted output
        # list_for_mse.append(np.mean((output_forward_after_backprop - y_train_holder) ** 2))
        # list_for_acc.append(calculate_accuracy(estimator, x_train_holder, y_train_holder))

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('fashion-mnist_train.csv' not in os.listdir('../Data') and
            'fashion-mnist_test.csv' not in os.listdir('../Data')):
        print('Train dataset loading.')
        url = "https://www.dropbox.com/s/5vg67ndkth17mvc/fashion-mnist_train.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_train.csv', 'wb').write(r.content)
        print('Loaded.')

        print('Test dataset loading.')
        url = "https://www.dropbox.com/s/9bj5a14unl5os6a/fashion-mnist_test.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_test.csv', 'wb').write(r.content)
        print('Loaded.')

    # Read train, test data.
    raw_train = pd.read_csv('../Data/fashion-mnist_train.csv')
    raw_test = pd.read_csv('../Data/fashion-mnist_test.csv')

    X_train = raw_train[raw_train.columns[1:]].values
    X_test = raw_test[raw_test.columns[1:]].values

    y_train = one_hot(raw_train['label'].values)
    y_test = one_hot(raw_test['label'].values)
    #print(y_train)

    # write your code here
    X_train_rescaled, X_test_rescaled = scale(X_train, X_test)

    # print(X_train_rescaled[2,778])
    # print(X_test_rescaled[0,774])
    # print(list(xavier(2, 3).flatten()))
    # print(sigmoid([-1,0,1,2]))
    # print([X_train_rescaled[2,778],X_test_rescaled[0,774]], list(xavier(2, 3).flatten()), sigmoid([-1,0,1,2]))
    # print(X_train[0])
    # input is 784 and 10 is output
    n_n_initialized = OneLayerNeural(784, 10)


    # Task 2
    # n_n_initialized.print_weights()
        # print(list(n_n_initialized.forward(X_train_rescaled[0]).flatten()) + list(n_n_initialized.forward(X_train_rescaled[1]).flatten()))

    # # Task 3
    # # print([mse(np.array([-1, 0, 1, 2]), np.array([4, 3, 2, 1]))])
    # # print(mse_derivative(np.array([-1, 0, 1, 2]), np.array([4, 3, 2, 1])))
    # # print(sigmoid_derivative(np.array([-1, 0, 1, 2])))
    #
    # # Forward step for the first two items of the training dataset
    # output_forward = n_n_initialized.forward(X_train_rescaled[:2, :])
    #
    # # Backpropagation step with alpha=0.1
    # loss_gradient = output_forward - y_train[:2, :]
    # learning_rate = 0.1
    # n_n_initialized.backprop(loss_gradient, learning_rate)
    #
    # # Forward step again for the same two items
    # output_forward_after_backprop = n_n_initialized.forward(X_train_rescaled[:2, :])
    #
    # # Calculate Mean Squared Error (MSE) between the actual y_train and the predicted output
    # mse_calced = np.mean((output_forward_after_backprop - y_train[:2, :]) ** 2)
    # # print([mse_calced])
    # print([mse(np.array([-1, 0, 1, 2]), np.array([4, 3, 2, 1]))],
    #       mse_derivative(np.array([-1, 0, 1, 2]), np.array([4, 3, 2, 1])).tolist(),
    #       sigmoid_derivative(sigmoid(np.array([-1, 0, 1, 2]))).tolist(),
    #       [mse_calced])
    # print("Task 3 acc: ", calculate_accuracy(n_n_initialized, X_train_rescaled[:2, :], y_train[:2, :]))

    # Task 4
    # print([calculate_accuracy(n_n_initialized, X_test_rescaled, y_test)])
    list_of_accuracies_for_epochs = []
    list_of_mse = []
    n_n_initialized_new = OneLayerNeural(784, 10)

    # single_epoch_training(n_n_initialized_new, 0.5, X_train_rescaled, y_train, list_of_mse,
    #                       list_of_accuracies_for_epochs)

    # Number of training epochs and batch size
    # Number of training epochs and batch size
    epochs = 20
    batch_size = 100

    # Split the data into batches
    for epoch in range(epochs):
        single_epoch_training(n_n_initialized_new, 0.5, X_train_rescaled, y_train, 100)

        # Calculate accuracy on the entire test set after each epoch
        list_of_accuracies_for_epochs.append(calculate_accuracy(n_n_initialized_new, X_test_rescaled, y_test))

    # print(list_of_mse)
    print([calculate_accuracy(n_n_initialized, X_test_rescaled, y_test)], list_of_accuracies_for_epochs)
