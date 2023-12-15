# run_coverage_scenario.py

import atomica as at
import os
import streamlit as st

if not os.path.exists('results'): os.makedirs('results')
if not os.path.exists('figs'): os.makedirs('figs')

@st.cache
def run_coverage_scenario(facility_code, start_year, coverage):
    P = at.Project(framework='carbomica_framework.xlsx', databook='books/carbomica_databook.xlsx',do_run=False)

    P.settings.sim_dt    = 1 # simulation timestep
    P.settings.sim_start = 2023 # simulation start year
    P.settings.sim_end   = 2024+5 # simulation end year

    progset = P.load_progbook('books/carbomica_progbook_{}.xlsx'.format(facility_code))

    coverage_scenario = {'electric_cars': at.TimeSeries(start_year,coverage)}

    instructions = at.ProgramInstructions(start_year=start_year, coverage=coverage_scenario)
    result_coverage = P.run_sim(P.parsets[0],P.progsets[0], progset_instructions=instructions, result_name='{:.0f}%'.format(coverage*100))
    result_coverage.export_raw('results/{}_coverage_raw.xlsx'.format(coverage*100))

    return result_coverage
