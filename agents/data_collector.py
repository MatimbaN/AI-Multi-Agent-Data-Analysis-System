import pandas as pd
import os

def data_collector_agent(state):
    try:
        vehicle_path = "Naamsa_Vehicle_Sales.csv"
        cpi_path = "CPI_Historic_Values_Zindi_Feb_23.csv"
        if not os.path.exists(vehicle_path):
            raise FileNotFoundError(f"File {vehicle_path} not found")
        if not os.path.exists(cpi_path):
            raise FileNotFoundError(f"File {cpi_path} not found")
        vehicle_df = pd.read_csv(vehicle_path)
        cpi_df = pd.read_csv(cpi_path)
        # Select only relevant columns
        cpi_df = cpi_df[['Month', 'Category', 'Value', 'Percentage Change (From Prior Month)']]
        state["vehicle_data"] = vehicle_df
        state["cpi_data"] = cpi_df
    except Exception as e:
        state["errors"].append(str(e))
    return state