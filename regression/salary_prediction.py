import os
import requests

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

# checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# download data if it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

list_of_mapes = [1.2099]
powers_to_check = [2, 3, 4]

def printing_best_mape(power_of):
    # read data
    data = pd.read_csv('../Data/data.csv')

    # write your code here
    # print(data.head())
    X, y = np.array(data["rating"]**power_of).reshape(-1, 1), np.array(data["salary"])


    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=100)

    model = LinearRegression()

    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)

    return mape(y_test, y_pred)

def multiple_vars_regression():
    # read data
    data = pd.read_csv('../Data/data.csv')

    # write your code here
    # print(data.head())
    list_of_data_parameters = [data[['rating', 'draft_round', 'age', 'experience', 'bmi']],
                               data[['draft_round', 'age', 'experience', 'bmi']],
                               data[['rating', 'draft_round', 'experience', 'bmi']],
                               data[['rating', 'draft_round', 'age', 'bmi']], data[['rating', 'draft_round', 'bmi']],
                               data[['draft_round', 'experience', 'bmi']], data[['draft_round', 'age', 'bmi']]]
    mapes_list = []
    mapes_list_medians = []
    mapes_list_zeros = []
    for dataset_x in list_of_data_parameters:
        X, y = np.array(dataset_x), np.array(data["salary"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=100)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mapes_list.append(mape(y_test, y_pred))

    print(mapes_list)

    print(round(min(mapes_list), 5))
    # In task 4 best are data[['rating', 'draft_round', 'bmi']] and 1.22789 MAPE

    # print(*model.coef_, sep = ",")

    # print(data.drop('salary',axis= 1).corr())
    # corelated are: rating, age, experience

def task5_best_mape():
    data = pd.read_csv('../Data/data.csv')
    X, y = np.array(data[['rating', 'draft_round', 'bmi']]), np.array(data["salary"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=100)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # print(y_pred)

    y_pred[y_pred < 0] = 0
    # print(y_pred)

    print(round(min([mape(y_test, y_pred)]), 5))

# print(round(model.intercept_, 5), round(model.coef_[0], 5), round(m_a_p_e, 5))

# Task 1 results: -92394937.42462 1322928.79254 1.2099

# for p in powers_to_check:
#     list_of_mapes.append(printing_best_mape(p))

# print(list_of_mapes)
# print(round(min(list_of_mapes), 5))

# Task 2 power of 3 is the best, 0.94182

# multiple_vars_regression()
if __name__ == '__main__':
    task5_best_mape()
# multiple_vars_regression()
