import pandas as pd #importing the pandas library and giving it an alias 'pd'
data = pd.read_csv('01BasicPython/utils/data.csv') #reading the csv file and storing it in a variable called 'data'
# print(data.head()) #printing the first 5 rows of the data
# print(data.info()) #printing the information about the data
# print(data.describe()) #printing the statistical summary of the data
# print(data['City'][0]) #printing the 'Name' column of the data
# print(data['State'][0]) #printing the 'Age' column of the data
# get max temparaturefor each city
# max_temp = data['Temperature'].max() #grouping the data by 'City' and getting the max temperature for each city
# # print(max_temp)
# print(data[data['Temperature'] == max_temp]) #printing the rows where the temperature is equal to the max temperature

# data['Temperature_C'] = (data['Temperature'] - 32) * 5.0/9.0 #converting the temperature from Fahrenheit to Celsius and storing it in a new column called 'Temperature_C'
# print(data) #printing the updated data with the new column 'Temperature_C'

print(data['Temperature'].mean()) #calculating the mean temperature and printing it