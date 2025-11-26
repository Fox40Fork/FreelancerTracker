import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def getUserByName(username: str):
    try:
        response = requests.get(f"{BASE_URL}/users/{username}")
        response.raise_for_status()  # Raises an exception for non-200 responses
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Response from server is not valid JSON.")
            st.write("Response text:", response.text[:500])  # Preview the response
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch users: {e}")
        return []

def login():
    def getUsers():
        try:
            response = requests.get(f"{BASE_URL}/users/")
            response.raise_for_status()  # Raises an exception for non-200 responses
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Response from server is not valid JSON.")
                st.write("Response text:", response.text[:500])  # Preview the response
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch users: {e}")
            return []

    def getSessions():
        try:
            response = requests.get(f"{BASE_URL}/sessions/")
            response.raise_for_status()  # Raises an exception for non-200 responses
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Response from server is not valid JSON.")
                st.write("Response text:", response.text[:500])  # Preview the response
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch sessions: {e}")
            return []

    def addSession(sessionData):
        try:
            response = requests.post(f"{BASE_URL}/sessions/", json=sessionData)
            response.raise_for_status()
            try:
                st.success(f"Session '{sessionData['username']}' added successfully!")
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Server response is not valid JSON.")
                st.write("Response text:", response.text[:500])
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to add session: {e}")
            return None

    st.subheader("Log In")

    usernameInput = st.text_input("Username")
    passwordInput = st.text_input("Password", type="password")

    if st.button("Log In"):
        users = getUsers()
        if any(u["username"] == usernameInput and u["password"] == passwordInput for u in users):
            st.write(f"Welcome, {usernameInput}!")
            sessionData = {
                "username": usernameInput
            }
            addSession(sessionData)
            st.session_state["username"] = usernameInput  # Store username in session state

            st.rerun()
        else:
            st.error("Invalid login")


def register():
    def getUsers():
        try:
            response = requests.get(f"{BASE_URL}/users/")
            response.raise_for_status()  # Raises an exception for non-200 responses
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Response from server is not valid JSON.")
                st.write("Response text:", response.text[:500])  # Preview the response
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch users: {e}")
            return []

    def addUser(userData):
        try:
            response = requests.post(f"{BASE_URL}/users/", json=userData)
            response.raise_for_status()
            try:
                st.success(f"User '{userData['username']}' added successfully!")
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Server response is not valid JSON.")
                st.write("Response text:", response.text[:500])
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to add user: {e}")
            return None

    st.subheader("Register")

    username = st.text_input("Enter your Username")
    email = st.text_input("Enter your E-Mail")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Register"):
        userInfo = {
            "username": username,
            "email": email,
            "password": password
        }
        addUser(userInfo)
        st.rerun()


def logout():
    def getSessions():
        try:
            response = requests.get(f"{BASE_URL}/sessions/")
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Response from server is not valid JSON.")
                st.write("Response text:", response.text[:500])
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch sessions: {e}")
            return []

    def deleteSession(session_id):
        try:
            response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
            response.raise_for_status()
            try:
                st.success("Logged out successfully!")
                return response.json()
            except requests.exceptions.JSONDecodeError:
                st.warning("Logged out successfully!")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to log out: {e}")
            return None

    if "username" in st.session_state:
        username = st.session_state["username"]
        sessions = getSessions()
        user_session = next((s for s in sessions if s.get("username") == username), None)
        if user_session and "id" in user_session:
            deleteSession(user_session["id"])
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    else:
        st.warning("No active session found.")


def is_authenticated():
    """Check if user has an active session"""
    if "username" not in st.session_state:
        return False

    try:
        response = requests.get(f"{BASE_URL}/sessions/")
        response.raise_for_status()
        sessions = response.json()
        return any(s.get("username") == st.session_state["username"] for s in sessions)
    except:
        return False