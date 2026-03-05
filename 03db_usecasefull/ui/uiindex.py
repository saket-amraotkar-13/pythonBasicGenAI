import streamlit as st
from db import init_db as dbconn


st.title("Welcome Learning Hub with Saket")

# num = st.number_input("Enter a number", min_value=0, max_value=100, value=50)
# if st.button("Click Me"):
#         if num >50:
#             st.write(f"The number {num} is greater than 50.")
#         elif num < 50:
#             st.write(f"The number {num} is less than 50.")
#         else:
#             st.write(f"The number {num} is equal to 50.")   

##connect to the database
@st.cache_resource
def get_db_connection():
    reuseconnn = dbconn.main()
    dbconn.create_table_course(reuseconnn)    
    course_data = {

        "UI5": {"credits": 3, "instructor": "Saket", "price": 500.00, "duration": 40},
        "Python": {"credits": 4, "instructor": "Saket", "price": 600.00, "duration": 50},
        "Data Science": {"credits": 5, "instructor": "SD", "price": 700.00, "duration": 60},
        "Machine Learning": {"credits": 4, "instructor": "SD", "price": 800.00, "duration": 70},
        "Cloud Computing": {"credits": 3, "instructor": "Saket", "price": 900.00, "duration": 80}
    }
    dbconn.execute_dml(reuseconnn, course_data)
    return reuseconnn

myconn = get_db_connection()

###design form  
with st.form("course_form"):
    st.subheader("Add a New Course")
    course_name = st.text_input("Course Name",placeholder="SAPUI5, Python, Data Science, Machine Learning, Cloud Computing")
    credits = st.number_input("Credits", min_value=1, max_value=10)
    instructor = st.text_input("Instructor")
    price = st.number_input("Price", min_value=0.0, step=0.01)
    duration = st.number_input("Duration (hours)", min_value=1, max_value=100)
    
    submitted = st.form_submit_button("👋Add Course")
    
    if submitted:
        course_data = {
            course_name: {"credits": credits, "instructor": instructor, "price": price, "duration": duration}
        }
        dbconn.execute_dml(myconn, course_data)
        st.success(f"Course '{course_name}' added successfully!")