#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from datetime import datetime, timedelta

# Create a directory for figures if it doesn't exist
import os
if not os.path.exists('figures'):
    os.makedirs('figures')

# Generate time series data
def generate_time_series():
    print("Generating time series plot...")
    # Create sample time series
    np.random.seed(42)
    days = 365
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(days)]
    temp_actual = 15 + 10 * np.sin(np.linspace(0, 2*np.pi, days)) + np.random.normal(0, 2, days)
    temp_model = 15 + 10 * np.sin(np.linspace(0, 2*np.pi, days)) + np.random.normal(0, 1, days)
    
    # Plot time series
    plt.figure(figsize=(10, 6))
    plt.plot(dates, temp_actual, 'b-', label='Observations')
    plt.plot(dates, temp_model, 'r-', label='Model')
    plt.title('Temperature Time Series: Model vs Observations')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('figures/time_series.pdf')
    plt.close()

# Generate error map
def generate_error_map():
    print("Generating error map...")
    # Create a spatial grid
    grid_size = 20
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Generate "true" data and "model" data with some differences
    Z_true = np.exp(-(X**2 + Y**2)/5) + 0.1*np.sin(X*Y)
    Z_model = np.exp(-(X**2 + Y**2)/5) + 0.05*np.cos(X*Y)
    Z_error = Z_true - Z_model
    
    # Plot error map
    plt.figure(figsize=(8, 7))
    plt.contourf(X, Y, Z_error, 20, cmap=cm.coolwarm)
    plt.colorbar(label='Error (Observation - Model)')
    plt.title('Spatial Error Distribution')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/error_map.pdf')
    plt.close()

# Generate table data
def generate_table_data():
    print("Generating table data...")
    # Create a sample statistical table
    regions = ['North', 'South', 'East', 'West', 'Central']
    metrics = ['RMSE', 'Correlation', 'Bias', 'Std Dev']
    
    # Generate random data for the table
    np.random.seed(42)
    data = {}
    for metric in metrics:
        if metric == 'Correlation':
            data[metric] = np.random.uniform(0.5, 0.95, len(regions))
        elif metric == 'Bias':
            data[metric] = np.random.uniform(-2, 2, len(regions))
        elif metric == 'RMSE':
            data[metric] = np.random.uniform(1, 5, len(regions))
        else:
            data[metric] = np.random.uniform(0.5, 3, len(regions))
    
    # Create a DataFrame
    df = pd.DataFrame(data, index=regions)
    
    # Format the table data
    formatted_table = df.round(2)
    
    # Save as CSV
    formatted_table.to_csv('figures/statistics.csv')
    
    # Generate LaTeX table code
    with open('figures/statistics_table.tex', 'w') as f:
        f.write('\\begin{table}[htbp]\n')
        f.write('\\centering\n')
        f.write('\\caption{Statistical Comparison by Region}\n')
        f.write('\\label{tab:statistics}\n')
        f.write('\\begin{tabular}{l' + 'r' * len(metrics) + '}\n')
        f.write('\\toprule\n')
        
        # Header row
        f.write('Region & ' + ' & '.join(metrics) + ' \\\\\n')
        f.write('\\midrule\n')
        
        # Data rows
        for region in regions:
            row_values = [f"{formatted_table.loc[region, metric]:.2f}" for metric in metrics]
            f.write(f"{region} & " + " & ".join(row_values) + " \\\\\n")
            
        f.write('\\bottomrule\n')
        f.write('\\end{tabular}\n')
        f.write('\\end{table}\n')

if __name__ == "__main__":
    print("Generating figures and data for the report...")
    generate_time_series()
    generate_error_map()
    generate_table_data()
    print("Done! All figures and data have been saved to the 'figures' directory.")
