#!/bin/bash
# build_report.sh - Script to automate the generation of a technical report

# Set colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting report generation workflow...${NC}"

# Create figures directory if it doesn't exist
if [ ! -d "figures" ]; then
    mkdir -p figures
    echo -e "${GREEN}Created figures directory${NC}"
fi

# Run Python script to generate figures and data
echo -e "${YELLOW}Generating figures and tables with Python...${NC}"
python3 generate_text_figures.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to generate figures${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully generated all figures and tables${NC}"

# Convert Markdown to HTML for easy viewing
if command -v pandoc &> /dev/null; then
    echo -e "${YELLOW}Converting Markdown to HTML with pandoc...${NC}"
    pandoc -f markdown -t html -o report.html report.md
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully generated HTML report: report.html${NC}"
    else
        echo -e "${RED}Warning: Failed to convert Markdown to HTML${NC}"
    fi
else
    echo -e "${YELLOW}Pandoc not found. Skipping Markdown to HTML conversion.${NC}"
    echo -e "${YELLOW}You can view the report directly in the Markdown file: report.md${NC}"
fi

# If LaTeX is available, try to generate a PDF
if command -v pdflatex &> /dev/null; then
    echo -e "${YELLOW}LaTeX found. Attempting to compile PDF report...${NC}"
    
    # Create a simple LaTeX wrapper for the content
    cat > report_latex.tex << EOL
\\documentclass[11pt,a4paper]{article}

% Packages
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{booktabs}
\\usepackage{geometry}
\\usepackage{verbatim}
\\usepackage{listings}
\\usepackage{xcolor}
\\usepackage{hyperref}

% Page layout
\\geometry{margin=1in}

% Title information
\\title{Technical Analysis Report}
\\author{Eduard Ruzga}
\\date{\\today}

\\begin{document}

\\maketitle

\\section*{Abstract}
This document demonstrates a workflow for generating reports that combine technical writing with programmatically generated figures and tables. This template is designed for scientific or technical reports that require data visualization and analysis.

\\section{Introduction}
This document demonstrates an automated workflow for creating technical reports with embedded figures and tables generated from data. It combines the power of programming for data analysis with document preparation.

The workflow consists of:
\\begin{itemize}
    \\item Python scripts that process data and generate figures
    \\item Document template that includes the generated figures
    \\item Shell script that automates the process
\\end{itemize}

\\section{Time Series Analysis}
Figure 1 shows a comparison between observed temperature data and model predictions over a one-month period. The model generally follows the seasonal pattern, but there are some discrepancies, particularly during extreme temperature events.

\\begin{verbatim}
EOL

    # Insert the time series visualization
    cat figures/time_series.txt >> report_latex.tex
    
    # Continue with the LaTeX document
    cat >> report_latex.tex << EOL
\\end{verbatim}

\\section{Spatial Error Analysis}
The spatial distribution of errors between observations and model predictions is shown below. Areas with positive values indicate where the model underestimates observations, while negative values show overestimation.

\\begin{verbatim}
EOL

    # Insert the error map visualization
    cat figures/error_map.txt >> report_latex.tex
    
    # Continue with the LaTeX document
    cat >> report_latex.tex << EOL
\\end{verbatim}

\\section{Regional Performance Statistics}
Table \\ref{tab:statistics} summarizes the model performance metrics across different regions. The metrics include Root Mean Square Error (RMSE), correlation coefficient, bias, and standard deviation.

EOL

    # Insert the LaTeX table
    cat figures/statistics_table.tex >> report_latex.tex
    
    # Finish the LaTeX document
    cat >> report_latex.tex << EOL

\\section{Conclusion}
This document demonstrated a workflow for generating technical reports with embedded figures and tables. This approach allows for:

\\begin{itemize}
    \\item Reproducible research and analysis
    \\item Consistent formatting and styling
    \\item Automated document generation
    \\item Version control of both code and document
\\end{itemize}

By combining programming for data analysis with document preparation, you can create professional-quality reports efficiently.

\\end{document}
EOL

    # Compile the LaTeX document
    pdflatex -interaction=nonstopmode report_latex.tex
    pdflatex -interaction=nonstopmode report_latex.tex
    
    if [ -f "report_latex.pdf" ]; then
        mv report_latex.pdf technical_report.pdf
        echo -e "${GREEN}Successfully generated PDF report: technical_report.pdf${NC}"
    else
        echo -e "${RED}Failed to generate PDF report${NC}"
    fi
    
    # Clean up auxiliary LaTeX files
    rm -f report_latex.aux report_latex.log report_latex.out
else
    echo -e "${YELLOW}LaTeX not found. Skipping PDF generation.${NC}"
fi

echo -e "${GREEN}Report generation workflow completed!${NC}"
echo -e "${GREEN}You can view the report in Markdown format: report.md${NC}"
