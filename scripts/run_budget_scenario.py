import streamlit as st
import atomica as at
import utils as ut
import os

st.title('Budget Scenario Runner')

# User input
facility_code = st.text_input('Enter facility code', 'AKHS_Mombasa')
start_year = st.number_input('Enter start year', min_value=2000, max_value=2100, value=2024, step=1)
investment = st.number_input('Enter investment', min_value=0.0, max_value=1e6, value=1e4, step=1e3)

# Atomica project definition
P = at.Project(framework='carbomica_framework.xlsx', databook='books/carbomica_databook.xlsx',do_run=False)

P.settings.sim_dt    = 1 # simulation timestep
P.settings.sim_start = 2023 # simulation start year
P.settings.sim_end   = 2024+5 # simulation end year

# Load program and define variables for program runs
progset = P.load_progbook('books/carbomica_progbook_{}.xlsx'.format(facility_code))

results_scenario = []

for prog in progset.programs:
    budget_scenario = {prog_all: 0 for prog_all in progset.programs}
    budget_scenario[prog] = investment
    instructions = at.ProgramInstructions(start_year=start_year, alloc=budget_scenario) # define program instructions
    result_budget = P.run_sim(parset='default',progset=P.progsets[0], progset_instructions=instructions, result_name=progset.programs[prog].label) # run budget scenario
    results_scenario.append(result_budget)

# Calculate emissions and allocation
emissions = ut.calc_emissions(results_scenario,start_year,facility_code,file_name='budget_scenario_Emissions_{}'.format(facility_code),title='CO2e emissions - fixed budget ($10,000.0)')
# allocation = ut.calc_allocation(results_scenario,file_name='allocation_budget_scen_{}'.format(facility_code)) # allocation

# Display results
st.write(emissions)
# st.write(allocation)