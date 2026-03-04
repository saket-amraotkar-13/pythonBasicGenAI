import streamlit as st
import middleware

st.title("UI Menu")

cusine = st.selectbox("Select Cuisine", ["Italian", "Chinese", "Mexican", "Indian"])
if st.button("Get Restaurant Recommendation"):
    if cusine:
        response = middleware.generate_restaurant_recommendation(cusine)    
        st.header("Restaurant Recommendation")
        st.write("Restaurant Recommendation:",response.get("restaurant_name"))
        st.write("***MENU ITEMS***")
        menu_items = response.get("menu").split(",")
        for item in menu_items:
            st.write(f"- {item.strip()}")
    else:
        st.write("Please select a cuisine.")
        