"""
Objective: Learn how to read, process, and manipulate CSV files, which is essential for handling your transaction data.

Exercise:

Task: Write a Python script that reads a CSV file containing transaction data 
with columns: date, amount, category, and description.
Goal: Your script should:
    Load the CSV file into memory.
    Print out each transaction in a readable format.
    Calculate the total amount spent for each category.
"""

import pandas as pd


data = pd.read_csv("finance_data.csv")

print(data)
