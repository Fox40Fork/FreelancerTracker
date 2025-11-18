import streamlit as st
import os
import requests

st.header("Create your account")

username = st.text_input("Username")
password = st.text_input("Password", type = "password")

BASE_URL = os.getenv("BASE_URL")

if st.button("Sign Up"):
    if username and password:
        try:
            response = requests.post(
                f"http://{BASE_URL}/signup",
                json = {"username" : username, "password" : password}
            )
            if response.status_code == 200:
                st.success("User created successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to reach the server: {e}")
    else:
        st.warning("Enter both username and password!")