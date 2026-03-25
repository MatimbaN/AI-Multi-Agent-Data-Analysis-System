import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
import shap
import numpy as np

def plot_cpi_trend(cpi_df):
    headline = cpi_df[cpi_df['Category'] == 'Headline_CPI'].sort_values('Month')
    plt.figure(figsize=(10, 5))
    plt.plot(headline['Month'], headline['Value'])
    plt.title('CPI Headline Trend Over Time')
    plt.xlabel('Month')
    plt.ylabel('CPI Value')
    plt.savefig('cpi_trend.png')
    plt.close()
    return "Plot saved as cpi_trend.png"

def plot_vehicle_trend(vehicle_df):
    # Assume Month is time, sort by Month
    vehicle_df = vehicle_df.sort_values('Month')
    plt.figure(figsize=(10, 5))
    plt.plot(vehicle_df['Month'], vehicle_df['Total_Local Sales'])
    plt.title('Vehicle Sales Trend Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Local Sales')
    plt.savefig('vehicle_trend.png')
    plt.close()
    return "Plot saved as vehicle_trend.png"

def compare_cpi_vs_vehicle(cpi_df, vehicle_df):
    # Align by time, but since different formats, perhaps plot separately or find common period
    # For simplicity, plot CPI headline and vehicle total side by side
    fig, ax1 = plt.subplots(figsize=(10, 5))
    headline = cpi_df[cpi_df['Category'] == 'Headline_CPI'].sort_values('Month')
    ax1.plot(headline['Month'], headline['Value'], 'b-', label='CPI')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('CPI Value', color='b')
    ax2 = ax1.twinx()
    vehicle_df = vehicle_df.sort_values('Month')
    ax2.plot(vehicle_df['Month'], vehicle_df['Total_Local Sales'], 'r-', label='Vehicle Sales')
    ax2.set_ylabel('Total Local Sales', color='r')
    plt.title('CPI vs Vehicle Sales Comparison')
    plt.savefig('compare_cpi_vehicle.png')
    plt.close()
    return "Plot saved as compare_cpi_vehicle.png"

def generate_histogram(cpi_df, column):
    data = cpi_df[cpi_df['Category'] == column]['Value']
    plt.figure(figsize=(10, 5))
    plt.hist(data, bins=20)
    plt.title(f'Histogram of {column}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.savefig('histogram.png')
    plt.close()
    return "Plot saved as histogram.png"

def generate_correlation_heatmap(cpi_df):
    # For CPI categories, pivot to have categories as columns
    pivot_df = cpi_df.pivot(index='Month', columns='Category', values='Value')
    corr = pivot_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('CPI Categories Correlation Heatmap')
    plt.savefig('correlation_heatmap.png')
    plt.close()
    return "Plot saved as correlation_heatmap.png"

def generate_prediction(cpi_df, vehicle_df):
    # Predict CPI headline using linear regression with time
    headline = cpi_df[cpi_df['Category'] == 'Headline_CPI'].sort_values('Month')
    if len(headline) < 2:
        return "Not enough data for prediction"
    headline = headline.copy()
    headline['time'] = np.arange(len(headline))
    X = headline[['time']]
    y = headline['Value']
    model = LinearRegression()
    model.fit(X, y)
    # Predict future 12 months
    future_time_df = pd.DataFrame({'time': np.arange(len(headline), len(headline) + 12)})
    predictions = model.predict(future_time_df)
    # Plot actual vs predicted
    plt.figure(figsize=(10, 5))
    plt.plot(headline['time'], y, label='Actual')
    plt.plot(future_time_df['time'], predictions, label='Predicted', linestyle='--')
    plt.title('Actual vs Predicted Headline CPI')
    plt.xlabel('Time')
    plt.ylabel('CPI Value')
    plt.legend()
    plt.savefig('cpi_prediction.png')
    plt.close()
    # SHAP for global importance
    try:
        explainer = shap.LinearExplainer(model, X)
        shap_values = explainer(X)
        plt.figure()
        shap.summary_plot(shap_values, X, show=False)
        plt.savefig('shap_summary.png')
        plt.close()
    except Exception as e:
        print(f"SHAP failed: {e}")
    # Scatter plot: vehicle sales vs transport CPI
    transport = cpi_df[cpi_df['Category'] == 'Transport'].sort_values('Month')
    if len(transport) == 0:
        return "No transport data"
    transport = transport.copy()
    transport['time'] = np.arange(len(transport))
    vehicle_df = vehicle_df.sort_values('Month')
    vehicle_subset = vehicle_df.head(len(transport))
    if len(vehicle_subset) != len(transport):
        return "Data length mismatch"
    plt.figure(figsize=(10, 5))
    plt.scatter(vehicle_subset['Total_Local Sales'], transport['Value'])
    # Trend line
    z = np.polyfit(vehicle_subset['Total_Local Sales'], transport['Value'], 1)
    p = np.poly1d(z)
    plt.plot(vehicle_subset['Total_Local Sales'], p(vehicle_subset['Total_Local Sales']), "r--")
    plt.title('Vehicle Sales vs Transport CPI (Correlation with Trend Line)')
    plt.xlabel('Total Local Sales')
    plt.ylabel('Transport CPI')
    plt.savefig('scatter_transport.png')
    plt.close()
    return "Prediction plot saved as cpi_prediction.png, SHAP saved as shap_summary.png, Scatter saved as scatter_transport.png"