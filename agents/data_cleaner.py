import pandas as pd
import numpy as np

def data_cleaner_agent(state):
    try:
        # Clean CPI
        cpi_df = state["cpi_data"].copy()
        cpi_df['Month'] = pd.to_datetime(cpi_df['Month'], format='%d-%m-%Y')
        cpi_df = cpi_df.dropna()
        cpi_df = cpi_df.drop_duplicates()
        # Outliers for Value and Percentage Change per category
        cleaned_cpi = []
        for cat in cpi_df['Category'].unique():
            cat_df = cpi_df[cpi_df['Category'] == cat]
            for col in ['Value', 'Percentage Change (From Prior Month)']:
                Q1 = cat_df[col].quantile(0.25)
                Q3 = cat_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                cat_df = cat_df[(cat_df[col] >= lower_bound) & (cat_df[col] <= upper_bound)]
            cleaned_cpi.append(cat_df)
        cpi_df = pd.concat(cleaned_cpi)
        state["cleaned_cpi_data"] = cpi_df

        # Clean Vehicle
        vehicle_df = state["vehicle_data"].copy()
        vehicle_df = vehicle_df.dropna()
        vehicle_df = vehicle_df.drop_duplicates()
        # Outliers for numerical columns
        numerical_cols = vehicle_df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            Q1 = vehicle_df[col].quantile(0.25)
            Q3 = vehicle_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            vehicle_df = vehicle_df[(vehicle_df[col] >= lower_bound) & (vehicle_df[col] <= upper_bound)]
        state["cleaned_vehicle_data"] = vehicle_df
    except Exception as e:
        state["errors"].append(str(e))
    return state