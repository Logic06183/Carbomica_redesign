# data_input_page.py
import streamlit as st
import pandas as pd

def show_data_input_page(session_state):
    st.title('Data Input Page')


# Initialize the dataframe within session state if it does not exist
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = pd.DataFrame(columns=[
        'Facility ID', 'Study Site', 'Emission Source', 'Emission Data',
        'Intervention', 'Effect Size', 'Implementation Cost', 'Maintenance Cost'
    ])

# Emission sources and interventions as provided
emission_sources = {
    "Grid_Electricity": "Grid Electricity",
    "Grid_Gas": "Grid gas",
    "Bottled_Gas": "Bottled gas (LPG)",
    "Liquid_Fuel": "Liquid fuel (Petrol or Diesel)",
    "Vehicle_Fuel_Owned": "Vehicle Fuel (Owned Vehicles)",
    "Business_Travel": "Business travel",
    "Anaesthetic_Gases": "Anaesthetic gases",
    "Refrigeration_Gases": "Refrigerants",
    "Waste_Management": "Waste",
    "Medical_Inhalers": "Inhalers"
}

intervention_options = {
    "Recycling_WasteSegregation": "Recycling & Segregation",
    "SolarSystem_Installation": "Solar Energy",
    "Efficient_Chillers_Upgrade": "Efficient Chillers",
    "Lighting_Efficiency": "LED & Lighting Control",
    "LowGWP_Refrigerants": "Low-GWP Refrigerants",
    "Hybrid_Car_Use": "Hybrid Vehicles",
    "LowGWP_Inhalers": "Low-GWP Inhalers",
    "LowGWP_AnaestheticGases": "Eco-friendly Anesthetics",
    "Staff_Training_Awareness": "Emissions Training & Conservation"
}

# Function to add or update facility data in the dataframe
def add_facility_data(facility_id, study_site, emission_source, emission_data):
    # Construct a new entry for the dataframe
    new_entry = {
        'Facility ID': facility_id,
        'Study Site': study_site,
        'Emission Source': emission_source,
        'Emission Data': emission_data
    }
    # Check if the facility ID already exists in the dataframe
    existing_entry = st.session_state['dataframe'][st.session_state['dataframe']['Facility ID'] == facility_id]
    if not existing_entry.empty:
        # Update existing entry
        st.session_state['dataframe'].loc[existing_entry.index] = pd.DataFrame(new_entry, index=existing_entry.index)
    else:
        # Add new entry
        st.session_state['dataframe'] = st.session_state['dataframe'].append(new_entry, ignore_index=True)

# Function to add or update intervention data in the dataframe
def add_intervention_data(facility_id, intervention, effect_size, implementation_cost, maintenance_cost):
    # Check if the facility ID already exists in the dataframe
    index = st.session_state['dataframe'][st.session_state['dataframe']['Facility ID'] == facility_id].index
    if index.empty:
        # If the facility doesn't exist, add a new entry for it
        add_facility_data(facility_id, "", "", "")
        index = st.session_state['dataframe'][st.session_state['dataframe']['Facility ID'] == facility_id].index
    
    # Update the intervention data for the facility
    st.session_state['dataframe'].loc[index, 'Intervention'] = intervention
    st.session_state['dataframe'].loc[index, 'Effect Size'] = effect_size
    st.session_state['dataframe'].loc[index, 'Implementation Cost'] = implementation_cost
    st.session_state['dataframe'].loc[index, 'Maintenance Cost'] = maintenance_cost

# Sidebar for facility data input
with st.sidebar:
    st.title('Facility Data Input')
    with st.form("facility_input_form"):
        facility_id = st.text_input("Facility Code Name", "facility_1")
        study_site = st.text_input("Study Site", "Facility 1")
        emission_source = st.selectbox("Emission Source", list(emission_sources.values()))
        emission_data = st.text_area("Emission Data")
        submit_facility = st.form_submit_button("Submit Facility Data")
        if submit_facility:
            add_facility_data(facility_id, study_site, emission_source, emission_data)

# Main page layout for intervention input
st.title('Interventions Input')
with st.form("intervention_input_form"):
    # Check for existing facilities before displaying the select box
    facility_options = st.session_state['dataframe']['Facility ID'].unique() if not st.session_state['dataframe'].empty else []
    facility_id = st.selectbox("Select Facility", options=facility_options)
    intervention = st.selectbox("Select Intervention", list(intervention_options.values()))
    effect_size = st.slider("Effect Size", 0.0, 1.0, 0.1)
    implementation_cost = st.number_input("Implementation Cost")
    maintenance_cost = st.number_input("Maintenance Cost")
    submit_intervention = st.form_submit_button("Submit Intervention Data")
    if submit_intervention:
        add_intervention_data(facility_id, intervention, effect_size, implementation_cost, maintenance_cost)

# Display the dataframe
st.write("Dataframe:", st.session_state['dataframe'])

# Optionally, save the dataframe to a CSV file
if st.button('Save Dataframe to CSV'):
    st.session_state['dataframe'].to_csv('facility_interventions.csv', index=False)
    st.success('Dataframe saved as facility_interventions.csv')
