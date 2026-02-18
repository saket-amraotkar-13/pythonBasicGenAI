import pandas as pd #importing the pandas library and giving it an alias 'pd'
data = pd.read_csv('01BasicPython/utils/data.csv') #reading the csv file and storing it in a variable called 'data'
print(data.head()) #printing the first 5 rows of the data