# scenario_analysis_page.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# scenario_analysis_page.py

import streamlit as st
from scripts.run_coverage_scenario import run_coverage_scenario

def main():
    facility_code = st.text_input("Enter facility code", "AKHS_Mombasa")
    start_year = st.number_input("Enter start year", min_value=2023, max_value=2030, value=2024)
    coverage = st.slider("Select coverage", min_value=0.0, max_value=1.0, value=1.0)

    if st.button("Run coverage scenario"):
        result_coverage = run_coverage_scenario(facility_code, start_year, coverage)
        st.write("Coverage scenario run complete. Check the 'results' folder for the output.")

if __name__ == "__main__":
    main()

# scenario_analysis_page.py

import streamlit as st
from scripts.run_coverage_scenario import run_coverage_scenario
from scripts.run_optimization import run_optimization

def main():
    facility_code = st.text_input("Enter facility code", "AKHS_Mombasa")
    start_year = st.number_input("Enter start year", min_value=2023, max_value=2030, value=2024)
    coverage = st.slider("Select coverage", min_value=0.0, max_value=1.0, value=1.0)
    budgets = [20e3, 50e3, 100e3]
    result_names = ['$20,000', '$50,000', '$100,000']

    if st.button("Run coverage scenario"):
        result_coverage = run_coverage_scenario(facility_code, start_year, coverage)
        st.write("Coverage scenario run complete. Check the 'results' folder for the output.")

    if st.button("Run optimization"):
        results_optimized = run_optimization(facility_code, start_year, budgets, result_names)
        st.write("Optimization run complete. Check the 'results' folder for the output.")
git init
if __name__ == "__main__":
    main()