import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


#Streamlite
st.set_page_config(
    page_title="Project 3 - Video Games Analysis - Webscrapping - Dashboarding ",
    page_icon=":smiley:",
    layout="wide",
)

dash = st.sidebar.radio(
    "What dashboard do you want to see ?",
    ('Name1', 'Name2', 'Name3', 'Advices before creating your game'))