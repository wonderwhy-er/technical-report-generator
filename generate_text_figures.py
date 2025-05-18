#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
import random
import math

# Create figures directory if it doesn't exist
if not os.path.exists('figures'):
    os.makedirs('figures')

print("Generating simple text-based visualizations...")

# Generate time series data
days = 30
start_date = datetime(2025, 4, 1)
dates = [start_date + timedelta(days=i) for i in range(days)]
temp_actual = [15 + 10 * math.sin(i/5) + random.uniform(-2, 2) for i in range(days)]
temp_model = [15 + 10 * math.sin(i/5) + random.uniform(-1, 1) for i in range(days)]

# Create a simple ASCII plot for time series
with open('figures/time_series.txt', 'w') as f:
    f.write("Temperature Time Series: Model vs Observations\n")
    f.write("=" * 60 + "\n\n")
    
    # Find the min and max values
    min_val = min(min(temp_actual), min(temp_model))
    max_val = max(max(temp_actual), max(temp_model))
    
    # Create the plot
    height = 20
    for h in range(height):
        line = ""
        level = max_val - (h * (max_val - min_val) / height)
        
        # Y-axis labels
        if h == 0:
            line += f"{max_val:.1f}°C |"
        elif h == height - 1:
            line += f"{min_val:.1f}°C |"
        elif h == height // 2:
            mid_val = (max_val + min_val) / 2
            line += f"{mid_val:.1f}°C |"
        else:
            line += "      |"
        
        # Plot points
        for i in range(days):
            if abs(temp_actual[i] - level) < (max_val - min_val) / height / 2:
                line += "o"  # Observation
            elif abs(temp_model[i] - level) < (max_val - min_val) / height / 2:
                line += "x"  # Model
            else:
                line += " "
        
        f.write(line + "\n")
    
    # X-axis
    f.write("      +" + "-" * days + "\n")
    
    # Date labels
    date_line = "       "
    for i in range(0, days, 5):
        date_str = dates[i].strftime("%d/%m")
        date_line += date_str
        if i + 5 < days:
            date_line += " " * (5 - len(date_str))
    
    f.write(date_line + "\n\n")
    f.write("Legend: o = Observations, x = Model\n")

print("✓ Generated time series visualization")

# Generate error map data
grid_size = 20
error_map = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Create a simple pattern
for i in range(grid_size):
    for j in range(grid_size):
        dist = math.sqrt((i - grid_size/2)**2 + (j - grid_size/2)**2)
        error_map[i][j] = 2 * math.sin(dist/2) * math.exp(-dist/10)

# Write error map to file
with open('figures/error_map.txt', 'w') as f:
    f.write("Spatial Error Distribution\n")
    f.write("=" * 60 + "\n\n")
    
    # Find min and max values
    flat_error = [error_map[i][j] for i in range(grid_size) for j in range(grid_size)]
    min_err = min(flat_error)
    max_err = max(flat_error)
    
    # Create ASCII representation
    for i in range(grid_size):
        row = ""
        for j in range(grid_size):
            err = error_map[i][j]
            if err > 0.66 * max_err:
                row += "+"  # High positive
            elif err > 0.33 * max_err:
                row += "o"  # Medium positive
            elif err > 0.05 * max_err:
                row += "."  # Low positive
            elif err < 0.66 * min_err:
                row += "#"  # High negative
            elif err < 0.33 * min_err:
                row += "X"  # Medium negative
            elif err < -0.05 * max_err:
                row += "x"  # Low negative
            else:
                row += " "  # Near zero
        f.write(row + "\n")
    
    f.write("\nLegend:\n")
    f.write("  + o . : Positive errors (observations > model)\n")
    f.write("  # X x : Negative errors (observations < model)\n")
    f.write(f"  Range: {min_err:.2f} to {max_err:.2f}\n")

print("✓ Generated error map visualization")

# Generate statistics table
regions = ['North', 'South', 'East', 'West', 'Central']
metrics = ['RMSE', 'Correlation', 'Bias', 'Std Dev']

# Generate random data for each region and metric
random.seed(42)  # For reproducibility
table_data = []

for region in regions:
    row = [region]
    # RMSE: typically 1-5
    row.append(round(random.uniform(1, 5), 2))
    # Correlation: 0-1
    row.append(round(random.uniform(0.5, 0.95), 2))
    # Bias: -2 to 2
    row.append(round(random.uniform(-2, 2), 2))
    # Std Dev: 0.5-3
    row.append(round(random.uniform(0.5, 3), 2))
    table_data.append(row)

# Write statistics table to file
with open('figures/statistics_table.txt', 'w') as f:
    f.write("Statistical Comparison by Region\n")
    f.write("=" * 60 + "\n\n")
    
    # Header
    f.write("| Region  | " + " | ".join(metrics) + " |\n")
    f.write("|" + "-" * 9 + "|" + "|".join(["-" * 12 for _ in metrics]) + "|\n")
    
    # Data rows
    for row in table_data:
        f.write(f"| {row[0]:<7} | {row[1]:<10} | {row[2]:<10} | {row[3]:<10} | {row[4]:<10} |\n")

print("✓ Generated statistics table")

# Create LaTeX table format for inclusion in LaTeX document
with open('figures/statistics_table.tex', 'w') as f:
    f.write("\\begin{table}[htbp]\n")
    f.write("\\centering\n")
    f.write("\\caption{Statistical Comparison by Region}\n")
    f.write("\\label{tab:statistics}\n")
    f.write("\\begin{tabular}{lrrrr}\n")
    f.write("\\toprule\n")
    
    # Header row
    f.write("Region & " + " & ".join(metrics) + " \\\\\n")
    f.write("\\midrule\n")
    
    # Data rows
    for row in table_data:
        f.write(f"{row[0]} & {row[1]} & {row[2]} & {row[3]} & {row[4]} \\\\\n")
        
    f.write("\\bottomrule\n")
    f.write("\\end{tabular}\n")
    f.write("\\end{table}\n")

print("✓ Generated LaTeX table code")

# Create a simple markdown report
with open('report.md', 'w') as f:
    f.write("# Technical Analysis Report\n\n")
    f.write(f"**Author:** Eduard Ruzga  \n**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
    
    f.write("## Abstract\n\n")
    f.write("This document demonstrates a workflow for generating reports that combine technical writing with programmatically generated figures and tables. This template is designed for scientific or technical reports that require data visualization and analysis.\n\n")
    
    f.write("## Introduction\n\n")
    f.write("This document demonstrates an automated workflow for creating technical reports with embedded figures and tables generated from data. It combines the power of programming for data analysis with document preparation.\n\n")
    
    f.write("The workflow consists of:\n")
    f.write("- Python scripts that process data and generate figures\n")
    f.write("- Document template that includes the generated figures\n")
    f.write("- Shell script that automates the process\n\n")
    
    f.write("## Time Series Analysis\n\n")
    f.write("Figure 1 shows a comparison between observed temperature data and model predictions over a one-month period. The model generally follows the seasonal pattern, but there are some discrepancies, particularly during extreme temperature events.\n\n")
    
    # Include the ASCII time series
    f.write("```\n")
    with open('figures/time_series.txt', 'r') as ts_file:
        f.write(ts_file.read())
    f.write("```\n\n")
    
    f.write("## Spatial Error Analysis\n\n")
    f.write("The spatial distribution of errors between observations and model predictions is shown in Figure 2. Areas with positive values indicate where the model underestimates observations, while negative values show overestimation.\n\n")
    
    # Include the ASCII error map
    f.write("```\n")
    with open('figures/error_map.txt', 'r') as em_file:
        f.write(em_file.read())
    f.write("```\n\n")
    
    f.write("## Regional Performance Statistics\n\n")
    f.write("Table 1 summarizes the model performance metrics across different regions. The metrics include Root Mean Square Error (RMSE), correlation coefficient, bias, and standard deviation.\n\n")
    
    # Include the markdown table
    with open('figures/statistics_table.txt', 'r') as st_file:
        # Skip the header lines
        lines = st_file.readlines()[3:]
        for line in lines:
            f.write(line)
    
    f.write("\n## Conclusion\n\n")
    f.write("This document demonstrated a workflow for generating technical reports with embedded figures and tables. This approach allows for:\n\n")
    f.write("- Reproducible research and analysis\n")
    f.write("- Consistent formatting and styling\n")
    f.write("- Automated document generation\n")
    f.write("- Version control of both code and document\n\n")
    
    f.write("By combining programming for data analysis with document preparation, you can create professional-quality reports efficiently.\n")

print("✓ Generated complete Markdown report")
print("\nAll done! The following files were created:")
print("- figures/time_series.txt: ASCII visualization of time series data")
print("- figures/error_map.txt: ASCII visualization of spatial error distribution")
print("- figures/statistics_table.txt: Markdown-formatted table")
print("- figures/statistics_table.tex: LaTeX-formatted table")
print("- report.md: Complete Markdown report incorporating all visualizations")
