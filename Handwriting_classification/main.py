# write your code here
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV

# Function to load data
def load_data():
    # Load the dataset, you might replace this with your actual data loading code
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    return x_train, y_train

# Task 3 function to input
def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    # here you fit the model
    clsf_model = model
    clsf_model.fit(features_train, target_train)
    # make a prediction
    calc_accuracy = clsf_model.score(features_test, target_test)
    # calculate accuracy and save it to score
    # print(f'Model: {model}\nAccuracy: {calc_accuracy}\n')
    return calc_accuracy


# # example
# # code
# fit_predict_eval(
#         model=KNeighborsClassifier(),
#         features_train=x_train,
#         features_test=x_test,
#         target_train=y_train,
#         target_test=y_test
#     )
# # output
# # >>> Model: KNeighborsClassifier()
# # >>> Accuracy: 0.1234

# Load the data
x_loaded, y_loaded = load_data()

# Reshape the features array
num_images, num_pixels_x, num_pixels_y = x_loaded.shape
x_loaded_reshaped = x_loaded.reshape(num_images, num_pixels_x * num_pixels_y)

# Task 1
# Print information about the dataset
# print("Classes:", np.unique(y_loaded))
# print("Features' shape:", x_loaded_reshaped.shape)
# print("Target's shape:", y_loaded.shape)
# print("min: {}, max: {}".format(np.min(x_loaded_reshaped), np.max(x_loaded_reshaped)))

# Task 2
x_train, x_test, y_train, y_test = train_test_split(x_loaded_reshaped[:6000, :], y_loaded[:6000],
                                                    test_size=0.3, random_state=40)

# print("x_train shape:", x_train.shape)
# print("x_test shape:", x_test.shape)
# print("y_train shape:", y_train.shape)
# print("y_test shape:", y_test.shape)
# print("Proportion of samples per class in train set:")
# # unique, counts = np.unique(y_train, return_counts=True)
# print(pd.Series(y_train).value_counts(normalize=True, sort=True))

# Task 3.
set_of_models = (KNeighborsClassifier(), DecisionTreeClassifier(random_state=40), LogisticRegression(random_state=40),
                 RandomForestClassifier(random_state=40))
set_of_models_labels = ("KNeighborsClassifier", "DecisionTreeClassifier", "LogisticRegression",
                 "RandomForestClassifier")
list_of_accuracies = []
# for test_default_model in set_of_models:
#     list_of_accuracies.append(fit_predict_eval(test_default_model, x_train, x_test, y_train, y_test))

# print(list_of_accuracies)
# print(round(max(list_of_accuracies), 3))
# print(set_of_models_labels[list_of_accuracies.index(max(list_of_accuracies))])

# print(f"The answer to the question: {set_of_models_labels[list_of_accuracies.index(max(list_of_accuracies))]} - {round(max(list_of_accuracies), 3)}")
#
# Model: KNeighborsClassifier()
# Accuracy: 0.935
#
# Model: DecisionTreeClassifier(random_state=40)
# Accuracy: 0.7605555555555555
#
# Model: LogisticRegression(random_state=40)
# Accuracy: 0.8738888888888889
#
# Model: RandomForestClassifier(random_state=40)
# Accuracy: 0.9394444444444444
#
# The answer to the question: RandomForestClassifier - 0.939


# Task 4

normalizer = Normalizer()
x_train_norm = normalizer.fit_transform(x_train)
# x_train_norm = pd.DataFrame(x_train_norm, columns=x_train.columns)

x_test_norm = normalizer.fit_transform(x_test)
# x_test_norm = pd.DataFrame(x_test_norm, columns=x_test.columns)

# for test_default_model in set_of_models:
#     list_of_accuracies.append(fit_predict_eval(test_default_model, x_train_norm, x_test_norm, y_train, y_test))
#
# # print(list_of_accuracies)
# # print(round(max(list_of_accuracies), 3))
# # print(set_of_models_labels[list_of_accuracies.index(max(list_of_accuracies))])
#
# print("The answer to the 1st question: yes")
# print("The answer to the 2nd question: KNeighborsClassifier-0.953, RandomForestClassifier-0.937")

# Task 5

# Finding optimal parameters for KNeighborsClassifier
# param_grid_kn = {'n_neighbors': [3, 4],
#               'weights': ['uniform', 'distance'],
#               'algorithm': ['auto', 'brute']}
#
# grid_search_kn = GridSearchCV(estimator=KNeighborsClassifier(), param_grid=param_grid_kn, scoring='accuracy', n_jobs=-1)
# grid_search_kn.fit(x_train_norm, y_train)
#
# print(grid_search_kn.best_estimator_)
# # KNeighborsClassifier(n_neighbors=4, weights='distance')

# Finding optimal parameters for Random Forest

# param_grid_rf = {'n_estimators': [300, 500],
#                  'max_features': ['sqrt', 'log2'],
#                  'class_weight': ['balanced', 'balanced_subsample']}
#
# grid_search_rf = GridSearchCV(estimator=RandomForestClassifier(random_state=40),
#                               param_grid=param_grid_rf, scoring='accuracy', n_jobs=-1)
# grid_search_rf.fit(x_train, y_train)
#
# print(grid_search_rf.best_estimator_)

# RF for normalized X
# RandomForestClassifier(class_weight='balanced_subsample', n_estimators=500,
#                        random_state=40)

# RF for not normalized X
# RandomForestClassifier(class_weight='balanced_subsample', n_estimators=500, random_state=40)

kn_accuracy = fit_predict_eval(KNeighborsClassifier(n_neighbors=4, weights='distance'),
                               x_train_norm, x_test_norm, y_train, y_test)
# print(kn_accuracy)

rf_accuracy_norm = fit_predict_eval(RandomForestClassifier(class_weight='balanced_subsample', n_estimators=500, random_state=40),
                               x_train_norm, x_test_norm, y_train, y_test)

# print(rf_accuracy_norm)

print(f'''K-nearest neighbours algorithm
best estimator: KNeighborsClassifier(n_neighbors=4, weights='distance')
accuracy: 0.9577777777777777

Random forest algorithm
best estimator: RandomForestClassifier(class_weight='balanced_subsample',
                       n_estimators=500, random_state=40)
accuracy: 0.94''')
