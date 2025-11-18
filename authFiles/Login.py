import streamlit as st
import sqlite3

st.header("Log In")
username = st.text_input("Username")
password = st.text_input("Password", type = "password")

if st.button("Log In"):
    #login logic here
    st.success(f"Welcome {username}!")

st.write("Don't have an account?")
st.page_link("pages/SignUp.py", label="Sign Up")