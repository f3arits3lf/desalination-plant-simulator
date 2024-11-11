import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Desalination Plant Simulator")

# Introduction
st.markdown("""
Welcome to the Desalination Plant Simulator! This tool allows you to model the desalination process and explore the effects of different inputs on energy costs, freshwater production, and waste brine generation. Adjust parameters such as feedwater salinity, treatment efficiency, and energy usage to observe the trade-offs involved in desalination.
""")

# Sidebar Inputs
st.sidebar.header("Plant Parameters")

# Basic Functional Plant Parameters (Always Enabled)
feedwater_salinity = st.sidebar.slider("Feedwater Salinity (ppm)", min_value=1000, max_value=50000, value=35000, step=500)
energy_use = st.sidebar.slider("Energy Use (kWh per cubic meter)", min_value=2.0, max_value=10.0, value=3.5, step=0.1)
treatment_efficiency = st.sidebar.slider("Treatment Efficiency (%)", min_value=30, max_value=90, value=50, step=5)
intake_flow_rate = st.sidebar.slider("Intake Flow Rate (cubic meters per hour)", min_value=50, max_value=500, value=100, step=10)

# Advanced Parameters with Optional Checkboxes
use_plant_capacity = st.sidebar.checkbox("Enable Plant Capacity Parameter", value=True)
if use_plant_capacity:
    plant_capacity = st.sidebar.slider("Plant Capacity (cubic meters per day)", min_value=1000, max_value=50000, value=10000, step=1000)
else:
    plant_capacity = None

use_carbon_emission_factor = st.sidebar.checkbox("Enable Carbon Emission Factor Parameter", value=True)
if use_carbon_emission_factor:
    carbon_emission_factor = st.sidebar.slider("Carbon Emission Factor (kg CO2 per kWh)", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
else:
    carbon_emission_factor = 0.0  # Assume no emissions if not enabled

use_chemical_cost = st.sidebar.checkbox("Enable Cost of Chemicals Parameter", value=True)
if use_chemical_cost:
    cost_of_chemicals_per_m3 = st.sidebar.slider("Cost of Chemicals per Cubic Meter ($/m^3)", min_value=0.05, max_value=1.0, value=0.25, step=0.05)
else:
    cost_of_chemicals_per_m3 = 0.0  # Assume no chemical cost if not enabled

use_labor_cost = st.sidebar.checkbox("Enable Labor Cost Parameter", value=True)
if use_labor_cost:
    labor_cost_per_day = st.sidebar.slider("Labor Cost per Day ($)", min_value=100, max_value=2000, value=500, step=50)
else:
    labor_cost_per_day = 0.0  # Assume no labor cost if not enabled

use_maintenance_cost = st.sidebar.checkbox("Enable Maintenance Cost Parameter", value=True)
if use_maintenance_cost:
    maintenance_cost_per_day = st.sidebar.slider("Maintenance Cost per Day ($)", min_value=50, max_value=1000, value=200, step=25)
else:
    maintenance_cost_per_day = 0.0  # Assume no maintenance cost if not enabled

# Constants
water_density = 1000  # kg/m^3
latent_heat_evaporation = 2260  # kJ/kg
energy_cost_per_kwh = 0.12  # $/kWh

# Enhanced Calculations
def calculate_outputs(feedwater_salinity, energy_use, treatment_efficiency, plant_capacity, intake_flow_rate, carbon_emission_factor, cost_of_chemicals_per_m3, labor_cost_per_day, maintenance_cost_per_day):
    """
    Calculate desalination plant outputs based on user inputs.
    """
    # Freshwater Production (cubic meters per hour)
    freshwater_production = treatment_efficiency / 100 * intake_flow_rate
    
    # Waste Brine Generation (cubic meters per hour)
    waste_brine = intake_flow_rate - freshwater_production
    
    # Energy Cost ($ per cubic meter of freshwater)
    energy_cost = energy_use * energy_cost_per_kwh
    
    # Daily Freshwater Production
    daily_freshwater_production = freshwater_production * 24
    
    # Carbon Emissions (kg CO2 per day)
    daily_energy_use = energy_use * daily_freshwater_production
    carbon_emissions = daily_energy_use * carbon_emission_factor
    
    # Chemical Cost ($ per day)
    chemical_cost = cost_of_chemicals_per_m3 * daily_freshwater_production
    
    # Total Operational Cost ($ per day)
    total_operational_cost = (energy_cost * daily_freshwater_production) + chemical_cost + labor_cost_per_day + maintenance_cost_per_day
    
    return freshwater_production, waste_brine, energy_cost, daily_freshwater_production, carbon_emissions, total_operational_cost

# Calculate Outputs
freshwater_production, waste_brine, energy_cost, daily_freshwater_production, carbon_emissions, total_operational_cost = calculate_outputs(feedwater_salinity, energy_use, treatment_efficiency, plant_capacity, intake_flow_rate, carbon_emission_factor, cost_of_chemicals_per_m3, labor_cost_per_day, maintenance_cost_per_day)

# Display Results
st.subheader("Simulation Results")

st.write(f"**Freshwater Production:** {freshwater_production:.2f} cubic meters per hour")
st.write(f"**Waste Brine Generation:** {waste_brine:.2f} cubic meters per hour")
st.write(f"**Energy Cost:** ${energy_cost:.2f} per cubic meter of freshwater")
st.write(f"**Daily Freshwater Production:** {daily_freshwater_production:.2f} cubic meters per day")
st.write(f"**Carbon Emissions:** {carbon_emissions:.2f} kg CO2 per day")
st.write(f"**Total Operational Cost:** ${total_operational_cost:.2f} per day")

# Plotting Trade-offs
st.subheader("Trade-off Visualization")

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Freshwater Production and Waste Brine Generation on the Primary Y-Axis
ax1.set_xlabel('Energy Use (kWh per cubic meter)')
ax1.set_ylabel('Flow Rate of Desalination Plant (m^3/hr)', color='tab:blue')
ax1.set_ylim(100, 200)  # Adjusted range for better clarity
energy_values = np.linspace(2, 10, 100)
freshwater_values = [calculate_outputs(feedwater_salinity, e, treatment_efficiency, plant_capacity, intake_flow_rate, carbon_emission_factor, cost_of_chemicals_per_m3, labor_cost_per_day, maintenance_cost_per_day)[0] for e in energy_values]
waste_brine_values = [calculate_outputs(feedwater_salinity, e, treatment_efficiency, plant_capacity, intake_flow_rate, carbon_emission_factor, cost_of_chemicals_per_m3, labor_cost_per_day, maintenance_cost_per_day)[1] for e in energy_values]
ax1.plot(energy_values, freshwater_values, label='Freshwater Production (m^3/hr)', color='b', linestyle='-', linewidth=2, marker='o')
ax1.plot(energy_values, waste_brine_values, label='Waste Brine Generation (m^3/hr)', color='r', linestyle='-.', linewidth=2, marker='s')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a Secondary Y-Axis for Energy Cost
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Energy Cost per Cubic Meter ($/m^3)', color='tab:green')
ax2.set_ylim(0, 1.5)  # Adjusted range for better clarity
energy_cost_values = [calculate_outputs(feedwater_salinity, e, treatment_efficiency, plant_capacity, intake_flow_rate, carbon_emission_factor, cost_of_chemicals_per_m3, labor_cost_per_day, maintenance_cost_per_day)[2] for e in energy_values]
ax2.plot(energy_values, energy_cost_values, label='Energy Cost ($/m^3)', color='g', linestyle='--', linewidth=2, marker='x')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Adding Legends
fig.tight_layout()  # to ensure everything fits without overlapping
ax1.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
ax2.legend(loc='upper right', bbox_to_anchor=(1.05, 0.9), borderaxespad=0.)

# Show Plot
st.pyplot(fig)

# Conclusion
st.markdown("""
### Key Takeaways:
- **Freshwater Production**: Increasing treatment efficiency leads to higher freshwater production but often requires more energy.
- **Waste Brine**: The amount of waste brine is inversely related to freshwater production and can be a major environmental concern.
- **Energy Cost**: There is a direct relationship between energy use and the cost of desalinated water, highlighting the importance of optimizing energy usage.
- **Carbon Emissions**: Higher energy use not only increases costs but also contributes to higher carbon emissions, making energy efficiency critical for sustainable desalination.
- **Operational Costs**: Chemical, labor, and maintenance costs are significant contributors to the overall cost, and optimizing these factors is crucial for economic sustainability.

Experiment with the sliders on the left to see how each factor affects the output and find the best balance for efficient desalination.
""")
