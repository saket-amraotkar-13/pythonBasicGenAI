

#string type
from datetime import datetime


name = "Saket Amraotkar"
#Integer
age = 18
#flot
height = 5.9
#boolean
isAlive = False

# print("Name", name, "is of type", type(name))
# print("Age", age, "is of type", type(age))
# print("height", height, "is of type", type(height))
# print("isAlive", isAlive, "is of type", type(isAlive))

#Type conversion
age_str = "56"
# print(age_str, type(age_str))

age_int = int(age_str)
# print(age_int, type(age_int))

#if condition

# if age > 18:
#     print(name,"is adult")
# elif age == 18:
#     print(name, "has just become adult")
# else:
#     print(name, 'is not adult')

#input from user
# new_age = input("enter your age: ")
# if int(new_age) > 18:
#     print(name,"is adult")
# elif int(new_age) == 18:
#     print(name, "has just become adult")
# else:
#     print(name, 'is not adult')

#concatename 1
age = 30
name = "saket"
height = 5.45
# print("Age of person is", age, "with height", height)

# concatename 2
# print(f"age of {name} is {age} with height: {height}")

#datetime
print(f"as of {datetime.now()} age of {name} is {age}")
