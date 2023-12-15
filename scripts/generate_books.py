import atomica as at
import pandas as pd
import os
import numpy as np
if not os.path.exists('books'): os.makedirs('books')
import pandas as pd
import atomica as at
'''
Script to generate a framework, databook and progbook.

'''
@st.cache
def create_framework(framework_template, sites_list, interventions_list, emissions_list):
    facilities = {}
    for site in sites_list.index:
        facilities[site] = {'label': sites_list.loc[site,'Display Name'], 'type': 'facilities'}

    interventions = {}
    for intervention in interventions_list.index:
        interventions[intervention] = interventions_list.loc[intervention,'Display Name']

    df_fw = pd.read_excel(pd.ExcelFile(framework_template), sheet_name=None)

    for i, emission in enumerate(emissions_list.index):
        emission_par = {'Code Name': emission+'_baseline', 
                    'Display Name': emissions_list.loc[emission,'Display Name'] + ' - baseline',
                    'Targetable': 'n',
                    'Databook Page': 'emission_sources'}
        emission_mult = {'Code Name': emission+'_mult', 
                    'Display Name': emissions_list.loc[emission,'Display Name'] + ' - multiplier',
                    'Targetable': 'y',
                    'Default Value': 0,
                    'Minimum Value': 0,
                    'Maximum Value': 1,
                    'Databook Page': 'targeted_pars'}
        emission_actual = {'Code Name': emission, 
                'Display Name': emissions_list.loc[emission,'Display Name'],
                'Targetable': 'n',
                'Population type': 'facilities',
                'Function': emission_par['Code Name']+'*(1-'+emission_mult['Code Name']+')'}
        df_fw['Parameters'] = pd.concat([df_fw['Parameters'], pd.DataFrame([emission_par])], ignore_index=True)
        df_fw['Parameters'] = pd.concat([df_fw['Parameters'], pd.DataFrame([emission_mult])], ignore_index=True)
        df_fw['Parameters'] = pd.concat([df_fw['Parameters'], pd.DataFrame([emission_actual])], ignore_index=True)

        if i == 0:
            df_fw['Parameters'].loc[df_fw['Parameters']['Code Name']=='co2e_emissions','Function'] = emission_actual['Code Name']
        else:
            df_fw['Parameters'].loc[df_fw['Parameters']['Code Name']=='co2e_emissions','Function'] += '+'+emission_actual['Code Name']
    
    with pd.ExcelWriter('carbomica_framework.xlsx') as writer:
        for sheet_name, df in df_fw.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


@st.cache
def create_databook(framework, facilities, db_data, data_years):
    F = at.ProjectFramework(framework)  # load framework

    D = at.ProjectData.new(framework=F, tvec=data_years, pops=facilities, transfers=0)

    for facility in facilities:
        D.tdve['facilities_number'].ts[facility] = at.TimeSeries(data_years, 1, units='Number')
        D.tdve['facilities_number'].write_assumption = True
        for parameter in db_data.columns:
            D.tdve[parameter+'_baseline'].ts[facility] = at.TimeSeries(data_years, db_data.loc[facility,parameter])
            D.tdve[parameter+'_baseline'].write_assumption = True
            
    D.save('books/carbomica_databook.xlsx')
    
#%% Step 3: generate empty progbooks in folder "templates/"

@st.cache
def create_progbook(framework, databook_name, facilities, interventions, target_pars_overall, effects, pb_costs_maintain, pb_costs_implement, data_years):
    P = at.Project(framework=framework, databook=databook_name, do_run=False)
    for facility in facilities:
        progbook_path = 'templates/carbomica_progbook_{}.xlsx'.format(facility)
        P.make_progbook(progbook_path, progs=interventions, data_start=data_years[0], data_end=data_years[-1])

    D = at.ProjectData.from_spreadsheet(databook_name, framework=framework) 

    for facility in facilities:
        P = at.ProgramSet.from_spreadsheet(spreadsheet='templates/carbomica_progbook_{}.xlsx'.format(facility), framework=framework, data=D, _allow_missing_data=True)
        for intervention in interventions:
            P.programs[intervention].target_pops = [facility]
            P.programs[intervention].target_comps = ['facilities_number']
            P.programs[intervention].unit_cost = at.TimeSeries(assumption=pb_costs_implement.loc[facility,intervention+'_cost']/len(data_years)+pb_costs_maintain.loc[facility,intervention+'_cost'], units='$/person/year')
            P.programs[intervention].spend_data = at.TimeSeries(data_years, 0, units='$/year')
            P.programs[intervention].capacity_constraint = at.TimeSeries(units='people')
            P.programs[intervention].coverage = at.TimeSeries(units='people')

        target_pars_overall_t = target_pars_overall.transpose()
        for par in target_pars_overall_t.index:
            target_interventions = target_pars_overall_t.columns[target_pars_overall_t.loc[par]=='y'].tolist()
            progs = {}
            for intervention in target_interventions:
                effect = effects.loc[facility,intervention+'_effect']
                progs[intervention] = effect
            P.covouts[(par+'_mult', facility)] = at.programs.Covout(par=par+'_mult',pop=facility,cov_interaction='random',baseline=0,progs=progs)
        P.programs[intervention].spend_data = at.TimeSeries(data_years,0, units='$/year') 
        P.save('books/carbomica_progbook_{}.xlsx'.format(facility)) 


