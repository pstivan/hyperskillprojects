import pandas as pd
import numpy as np
import requests
import os

# scroll down to the bottom to implement your solution

# Task 4 Function
def count_bigger_5(series):
    return (series > 5).sum()

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    # Task 1 changing indexes
    df_a = pd.read_xml('../Data/A_office_data.xml')
    df_b = pd.read_xml('../Data/B_office_data.xml')
    df_hr = pd.read_xml('../Data/hr_data.xml')
    df_a['ind'] = "A" + df_a['employee_office_id'].astype(str)
    df_b['ind'] = "B" + df_b['employee_office_id'].astype(str)
    df_a_i = df_a.set_index('ind')
    df_b_i = df_b.set_index('ind')
    df_hr_i = df_hr.set_index("employee_id")

    # print(df_a_i.head())
    # print(df_b_i.head())
    # print(df_hr_i.head())

    # print(df_a_i.index.tolist())
    # print(df_b_i.index.tolist())
    # print(df_hr_i.index.tolist())

    # Task 2 merging dataframes

    # Concating dataframes of offices A and B
    df_a_b_concat = pd.concat([df_a_i, df_b_i])
    # print(df_a_b_concat.head())

    # Merging HR dataframe with concatenated table of offices A-B and HR
    df_a_b_hr_merged = df_a_b_concat.merge(df_hr_i, how='left', left_index=True, right_index=True,
                                           indicator=True)
    df_a_b_hr_merged.dropna(inplace=True)
    df_a_b_hr_merged.drop(["employee_office_id", "_merge"], axis=1, inplace=True)
    df_a_b_hr_merged.sort_index(inplace=True)
    # print(df_a_b_hr_merged.head())
    # print(df_a_b_hr_merged.index.tolist())
    # print(df_a_b_hr_merged.columns.tolist())

    # Task 3
    # Answer the questions from the description using the pandas built-in methods.
    # Here is a little explanation for each question:

    # 1. What are the departments of the top ten employees in terms of working hours?
    # Use average_monthly_hours column to sort the dataset in descending order and
    # output a Python list of departments' names;
    # print(df_a_b_hr_merged.sort_values(by='average_monthly_hours', ascending=False).Department.head(10).tolist())

    # 2. What is the total number of projects on which IT department employees with low salaries have worked?
    # Use Department and salary ('low') with corresponding values to filter the dataset. You will need to sum up the
    # values from the number_project column and output a number;
    # print(df_a_b_hr_merged.query("Department == 'IT' & salary == 'low'").number_project.sum())

    # 3. What are the last evaluation scores and the satisfaction levels of the employees A4, B7064, and A3033?
    # Objectives
    # Find last_evaluation and satisfaction_level values for the employees A4, B7064, and A3033.
    # Output a Python list where each entry is a list of values of the last evaluation score and
    # the satisfaction level of an employee. The data for each employee should be specified in the same order
    # as the employees' IDs in the question above. Apply the .loc method of pandas to answer the question!

    list_of_ind = ["A4", "B7064", "A3033"]
    columns = ['last_evaluation', 'satisfaction_level']
    # print(df_a_b_hr_merged.loc[list_of_ind][columns].values.tolist())

    # 4
    # The HR boss asks for the following metrics:
    #
    # the median number of projects the employees in a group worked on, and how many employees worked on more than five projects;
    # the mean and median time spent in the company;
    # the share of employees who've had work accidents;
    # the mean and standard deviation of the last evaluation score.
    # Write the count_bigger_5 function that counts the number of employees who worked on more than five projects. You will then use it in the agg() method to calculate the metric from the first point in the Description section;
    # Use groupby() with left column and agg() to generate a table with metrics according to the boss's needs. Round all the numbers to two decimals. To round numbers to the second decimal place, you can apply the round(2) method to a DataFrame;
    # Print the resulting table as a Python dictionary. To do so, use the to_dict() method.
    result = df_a_b_hr_merged.groupby('left').agg(
        {'number_project': ['median', count_bigger_5],
         'time_spend_company': ['mean', 'median'],
         'Work_accident': 'mean',
         'last_evaluation': ['mean', 'std']
         }
    ).round(2).to_dict()
    # print(result)

    # Task 5
    # Use df.pivot_table() to generate the first pivot table: Department as index, left and
    # salary as columns, average_monthly_hours as values. Output median values in the table.

    pivot_table_1 = df_a_b_hr_merged.pivot_table(index='Department', columns=['left', 'salary'],
    values='average_monthly_hours', aggfunc='median')

    filtered_pivot_table_1 = pivot_table_1[((pivot_table_1[(0, 'high')] < pivot_table_1[(0, 'medium')]))
                                         | ((pivot_table_1[(1, 'low')] < pivot_table_1[(1, 'high')]))]

    print(filtered_pivot_table_1.to_dict())

    # Use df.pivot_table() to generate the second pivot table:
    # time_spend_company as index, promotion_last_5years as column, satisfaction_level and last_evaluation as values.
    # Output the min, max, and mean values in the table.
    # Use the search methods to subset the data as requested in the Description section.
    # Round all the numbers to two decimals;
    # Print two resulting DataFrames as Python dictionaries. To do so, use the to_dict() method.

    pivot_table_2 = df_a_b_hr_merged.pivot_table(index='time_spend_company', columns='promotion_last_5years',
                                                 values=['satisfaction_level', 'last_evaluation'],
                                                 aggfunc=['min', 'max', 'mean'])

    filtered_pivot_table_2 = pivot_table_2[
        pivot_table_2[('mean', 'last_evaluation', 0)] > pivot_table_2[('mean', 'last_evaluation', 1)]]

    print(filtered_pivot_table_2.to_dict())
