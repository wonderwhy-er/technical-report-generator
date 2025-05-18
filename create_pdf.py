#!/usr/bin/env python3
import os
import sys
import subprocess
import importlib.util

# Check if we have the required libraries
has_pdfkit = importlib.util.find_spec("pdfkit") is not None
has_weasyprint = importlib.util.find_spec("weasyprint") is not None

print("Creating PDF from our report...")

# Function to read file content
def read_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Read our content files
time_series = read_file('figures/time_series.txt')
error_map = read_file('figures/error_map.txt')

# Parse statistics table
stats_table_rows = []
try:
    stats_text = read_file('figures/statistics_table.txt')
    lines = stats_text.split('\n')
    # Skip header lines
    data_lines = [line for line in lines if line.startswith('|') and not line.startswith('|---')]
    
    # Skip the header row
    for line in data_lines[1:]:
        cells = line.split('|')
        # Filter out empty cells (start and end of line)
        cells = [cell.strip() for cell in cells if cell.strip()]
        if cells:
            stats_table_rows.append(cells)
except Exception as e:
    print(f"Error parsing statistics table: {e}")

# Create an updated HTML file with the content directly embedded
html_content = read_file('report.html')

# Replace placeholders with actual content
if time_series:
    html_content = html_content.replace('<pre id="time-series"></pre>', f'<pre id="time-series">{time_series}</pre>')

if error_map:
    html_content = html_content.replace('<pre id="error-map"></pre>', f'<pre id="error-map">{error_map}</pre>')

# Build table HTML
if stats_table_rows:
    table_html = ""
    for row in stats_table_rows:
        table_html += "<tr>"
        for cell in row:
            table_html += f"<td>{cell}</td>"
        table_html += "</tr>\n"
    
    html_content = html_content.replace('<tbody id="statistics-table">\n            <!-- Table content will be inserted here by script -->\n        </tbody>', 
                                       f'<tbody id="statistics-table">\n            {table_html}\n        </tbody>')

# Also remove the script section since we no longer need it
script_start = html_content.find('<script>')
script_end = html_content.find('</script>') + 9
if script_start > 0 and script_end > 0:
    html_content = html_content[:script_start] + html_content[script_end:]

# Write the updated HTML
with open('report_static.html', 'w') as f:
    f.write(html_content)

print("✓ Created static HTML file: report_static.html")

# Try different approaches to convert to PDF
pdf_created = False

# Approach 1: Use pdfkit if available
if has_pdfkit:
    try:
        import pdfkit
        pdfkit.from_file('report_static.html', 'technical_report.pdf')
        print("✓ PDF created using pdfkit: technical_report.pdf")
        pdf_created = True
    except Exception as e:
        print(f"Error creating PDF with pdfkit: {e}")

# Approach 2: Use weasyprint if available
if not pdf_created and has_weasyprint:
    try:
        from weasyprint import HTML
        HTML('report_static.html').write_pdf('technical_report.pdf')
        print("✓ PDF created using weasyprint: technical_report.pdf")
        pdf_created = True
    except Exception as e:
        print(f"Error creating PDF with weasyprint: {e}")

# Approach 3: Try wkhtmltopdf command-line tool
if not pdf_created:
    try:
        subprocess.run(['wkhtmltopdf', 'report_static.html', 'technical_report.pdf'], 
                      check=True, capture_output=True)
        print("✓ PDF created using wkhtmltopdf: technical_report.pdf")
        pdf_created = True
    except Exception as e:
        print(f"Error creating PDF with wkhtmltopdf: {e}")

# Approach 4: Try headless Chrome if available
if not pdf_created:
    try:
        chrome_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser'
        ]
        
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            cmd = [
                chrome_path,
                '--headless',
                '--disable-gpu',
                '--print-to-pdf=technical_report.pdf',
                f'file://{os.path.abspath("report_static.html")}'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print("✓ PDF created using headless Chrome: technical_report.pdf")
            pdf_created = True
    except Exception as e:
        print(f"Error creating PDF with Chrome: {e}")

if not pdf_created:
    print("\n⚠️ Could not create PDF automatically.")
    print("You can manually convert the HTML file to PDF using:")
    print("1. Open report_static.html in a browser")
    print("2. Use the browser's print function (Ctrl+P or Cmd+P)")
    print("3. Select 'Save as PDF' as the destination")
else:
    print("\n✓ PDF creation completed successfully!")
