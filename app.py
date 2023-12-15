# app.py
import streamlit as st


# In app.py
from data_input_page import show_data_input_page
from scenario_analysis_page import show_scenario_analysis_page


# Define the pages in the app
PAGES = {
    "Data Input": show_data_input_page,
    "Scenario Analysis": show_scenario_analysis_page
}

# Sidebar for page navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Display the selected page with the session state as an input
page = PAGES[selection]
page(st.session_state)
