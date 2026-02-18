

from locale import currency


course_catalog = {
    "SAPUI5": {"Trainer": "Saket", "Duration": "4 weeks", "Level": "Beginner", "Price": "500", "Currency": "USD"},
    "Python": {"Trainer": "Mangesh", "Duration": "8 weeks", "Level": "Intermediate", "Price": "750", "Currency": "USD"},
    "CAPM": {"Trainer": "Saket", "Duration": "6 weeks", "Level": "Advanced", "Price": "600", "Currency": "USD"},
    "RAP": {"Trainer": "Saket", "Duration": "5 weeks", "Level": "Beginner", "Price": "550", 	"Currency": 	"USD"},
    "Fiori": {"Trainer": 	"Mangesh", 	"Duration":"3 weeks","Level":"Intermediate","Price":"400","Currency":"USD"},
   	"Ariba":{"Trainer":"Thiruna","Duration":"7 weeks","Level":"Advanced","Price":"700","Currency":"USD"},
}

# print(course_catalog) #printing the course catalog
# print(course_catalog["Python"]) #printing the details of the Python course
# print(course_catalog["Python"]["Trainer"]) #printing the trainer of the Python course
# print(course_catalog["Python"]["Duration"]) #printing the duration of the Python course
# print(course_catalog["Python"]["Level"]) #printing the level of the Python course
# print(course_catalog["Python"]["Price"]) #printing the price of the Python course 

selected_course = []

while True:
    course_name = input("Enter the course name you want to enroll in (or 'exit' to EXIT): ").strip().upper() #taking input from the user and converting it to uppercase 
    if course_name == 'exit' or course_name == 'EXIT':
        break
    elif course_name in course_catalog:
        selected_course.append(course_name)
        print(f"You have selected the {course_name} course.")
    else:
        print(f"Course {course_name} not found. Please try again.")

print("\nYou have enrolled in the following courses:")
total_price = 0

for indx,course_name in enumerate(selected_course, start=1):
    details = course_catalog[course_name]
    print(f"{indx}. {course_name}: Trainer: {details['Trainer']}, Duration: {details['Duration']}, Level: {details['Level']},Price: {details['Price']}, Currency: {details['Currency']}")
    total_price += int(details['Price'])

print(f"\nGrand Total Price: {total_price} {details['Currency']}")