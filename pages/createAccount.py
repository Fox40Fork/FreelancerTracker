import streamlit as st

st.title("Create an account")

username = st.text_input("Username")
email = st.text_input("E-Mail")
password = st.text_input("Password", type = "password")
checkPassword = st.text_input("Confirm your password", type = "password") #Kod za ovo ću kasnije dovršiti

if st.button("Create"): #i za ovo
    pass