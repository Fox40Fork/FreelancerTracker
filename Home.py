import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

BASE_URL = os.getenv("BASE_URL")

st.set_page_config(
    page_title = "Home"
)

st.header("Home")
st.write("The home page for the Freelancer Invoice/Income Tracker app.")

st.sidebar.warning("You can navigate through the pages here.")