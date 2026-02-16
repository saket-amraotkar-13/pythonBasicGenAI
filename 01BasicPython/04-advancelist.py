# list with text
# my_list = ["apple", "banana", "cherry", "date", "elderberry","raspberry"] #creating a list of fruits
# print(my_list) #printing the list
# print(my_list[0]) #printing the first element of the list   
# print(my_list[1]) #printing the second element of the list
# print(my_list[2]) #printing the third element of the list   
# print(my_list[-1]) #printing the last element of the list
# print(my_list[-3]) #printing the second last element of the list
# print(my_list[1:4]) #printing the elements from index 1 to 3 (4 is exclusive)
# print(my_list[:3]) #printing the first three elements of the list   
# print(my_list[2:]) #printing the elements from index 2 to the end of the list
# print(my_list[::2]) #printing every second element of the list
# my_list.append("fig") #adding an element to the end of the list
# print(my_list) #printing the list after adding an element
# my_list.insert(2, "grape") #inserting an element at index 2
# print(my_list) #printing the list after inserting an element
# my_list.remove("banana") #removing an element from the list
# print(my_list) #printing the list after removing an element
# my_list.pop() #removing the last element from the list
# print(my_list) #printing the list after popping an element
# my_list.pop(1) #removing the element at index 1
# print(my_list) #printing the list after popping an element at index 1
# my_list[0] = "avocado" #changing the first element of the list
# print(my_list) #printing the list after changing an element
# len(my_list) #finding the length of the list
# print(len(my_list)) #printing the length of the list

# if "cherry1" in my_list: #checking if an element is in the list
#     print("cherry is in the list") #printing if cherry is in the list
# else:    print("cherry is not in the list") #printing if cherry is not in the list

# my_numbers = [1, 2, 3, 4, 5]
# print(my_numbers) #printing the list of numbers
# print(my_numbers[0]) #printing the first element of the list  
# sq_numbers = [x**2 for x in my_numbers] #creating a new list with the squares of the numbers in the original list using list comprehension
# print(sq_numbers) #printing the list of squared numbers

###set
# my_set = {"apple", "banana", "cherry", "date", "elderberry","raspberry"} #creating a set of fruits
# print(my_set) #printing the set   
# my_set.add("fig") #adding an element to the set
# print(my_set) #printing the set after adding an element

# ###set does not allow duplicate elements
# my_set.add("apple") #adding a duplicate element to the set  
# print(my_set) #printing the set after adding a duplicate element, it will not be added to the set

##set union and intersection
# set1 = {"apple", "banana", "cherry"}
# set2 = {"banana", "date", "elderberry"} 
# union_set = set1.union(set2) #finding the union of two sets
# print(union_set) #printing the union of two sets - unique elements from both sets
# intersection_set = set1.intersection(set2) #finding the intersection of two sets - common elements from both sets
# print(intersection_set) #printing the intersection of two sets

# print(set1.difference(set2)) #finding the difference of two sets - elements in set1 that are not in set2
# print(set2.difference(set1)) #finding the difference of two sets - elements in set


# my_fruits = {"apple", "banana", "cherry", "date", "elderberry","raspberry"} #creating a set of fruits
# print(my_fruits) #printing the set of fruits
# print(list(my_fruits)[0]) #printing the first element of the set (converted to list)
# print(list(my_fruits)[1]) #printing the second element of the set (converted to list)   
# my_fruits.add("fig") #adding an element to the set
# print(my_fruits) #printing the set after adding an element   

###tupple
# my_tuple = ("apple", "banana", "cherry", "date", "elderberry","raspberry") #creating a tuple of fruits
# print(my_tuple) #printing the tuple of fruits
# print(my_tuple[0]) #printing the first element of the tuple
# print(my_tuple[1]) #printing the second element of the tuple    
# my_tuple[0] = "avocado" #trying to change the first element of the tuple, it will raise an error because tuples are immutable
# unpacked_tuple = ("apple", "banana", "cherry","appl") #creating a tuple of fruits
# # fruit1, fruit2, fruit3, fruit4 = unpacked_tuple #unpacking the tuple into individual variables
# # print(fruit1,fruit2,fruit3,fruit4) #printing the first variable    

# print(unpacked_tuple.count("apple")) #counting the number of times "apple" appears in the tuple
# print(unpacked_tuple.index("banana")) #finding the index of "banana" in the tuple
# a, b, c = unpacked_tuple[:3]#unpacking the tuple into individual variables
# print(a, b, c) #printing the first three variables

# mixed_tuple = ("apple", 1, "banana", 2, "cherry", True) #creating a tuple with mixed data types
# print(mixed_tuple) #printing the tuple with mixed data types


###dictionary are like json objects, they are key-value pairs
# my_dict = {"name": "Alice", "age": 30, "city": "New York"} #creating a dictionary with key-value pairs
# print(my_dict) #printing the dictionary

emp_data = {"name": "John Doe", "age": 35, "position": "Software Engineer", "skills": ["Python", "JavaScript", "SQL"]} #creating a dictionary with nested data
# print(emp_data) #printing the dictionary with nested data

    # print(emp_data["name"]) #printing the value of the "name" key in the dictionary
    # print(emp_data["skills"]) #printing the value of the "skills" key in the dictionary

# print(emp_data["skills"][0]) #printing the first skill in the "skills" list in the dictionary
# print(emp_data["skills"][1]) #printing the second skill in the "skills" list in the dictionary
# print("emp age is:",emp_data.get("age")) #printing the value of the "age" key in the dictionary using get method
# print("emp skiils are:",emp_data.get("skills")) #printing the value of the "skills" key in the dictionary using get method
        # print("emp first skill is:",emp_data.get("skills")[0]) #printing the first skill in the "skills" list in the dictionary using get method
        # emp_data["skills"].append("Java") #adding a new skill to the "skills" list in the dictionary
        # print("emp skills after adding new skill:",emp_data.get("skills")) #printing the value
emp_data["salary"] = 100000 #adding a new key-value pair to the dictionary
# print("emp data after adding salary:",emp_data) #printing the dictionary after adding a new
# for key in emp_data: #iterating through the keys in the dictionary
#     # print(key) #printing the keys in the dictionary
#     print(emp_data[key]) #printing the values in the dictionary using the keys  clear

# delete item from disctionary
del emp_data["age"] #deleting the "age" key-value pair from the dictionary
print("emp data after deleting age:",emp_data) #printing the dictionary after deleting a key-value pair
