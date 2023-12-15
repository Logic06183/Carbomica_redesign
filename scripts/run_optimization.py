# run_optimization.py

import atomica as at
import numpy as np
import os
import streamlit as st

if not os.path.exists('results'): os.makedirs('results')
if not os.path.exists('figs'): os.makedirs('figs')

@st.cache
def run_optimization(facility_code, start_year, budgets, result_names):
    P = at.Project(framework='carbomica_framework.xlsx', databook='books/carbomica_databook.xlsx',do_run=False)

    P.settings.sim_dt    = 1 # simulation timestep
    P.settings.sim_start = 2023 # simulation start year
    P.settings.sim_end   = 2024+5 # simulation end year

    progset = P.load_progbook('books/carbomica_progbook_{}.xlsx'.format(facility_code))

    instructions = at.ProgramInstructions(alloc=P.progsets[0], start_year=start_year)

    adjustments = [at.SpendingAdjustment(prog, start_year, 'abs', 0.0, 10e6) for prog in progset.programs]

    measurables = [at.MinimizeMeasurable('co2e_emissions',start_year)]

    np.random.seed(4)

    results_optimized = []
    for budget, name in zip(budgets, result_names):
        constraints = at.TotalSpendConstraint(total_spend=budget, t=start_year)
        optimization = at.Optimization(name='default', method='pso', adjustments=adjustments, measurables=measurables, constraints=constraints)
        optimized_instructions = at.optimize(P, optimization, P.parsets[0],P.progsets[0], instructions=instructions, optim_args={"maxiter": 10})
        result_optimized = P.run_sim(P.parsets[0],P.progsets[0], progset_instructions=optimized_instructions)
        result_optimized.name = name
        results_optimized.append(result_optimized)

    return results_optimized