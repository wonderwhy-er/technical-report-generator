# Technical Report Generator

This is a proof-of-concept for generating technical reports that combine writing with programmatically generated figures and tables. It demonstrates a workflow suitable for scientific papers, technical documentation, or data analysis reports.

This project was created using [Desktop Commander](https://desktopcommander.app/) as an exploration for the article [Hi Eduard, thanks very much for replying](https://medium.com/@tdcwilliams/hi-eduard-thanks-very-much-for-replying-2c252f6e3546).

You can find the source code on GitHub: [github.com/wonderwhy-er/technical-report-generator](https://github.com/wonderwhy-er/technical-report-generator)

This project was generated through a conversation with Claude AI: [View the Claude chat](https://claude.ai/share/e28ba915-3df0-4bd8-8038-e581acd39051)

## Components

1. **generate_figures.py**: Python script that creates sample data visualizations and generates a LaTeX table
2. **report_template.tex**: LaTeX template for the report, with placeholders for the generated figures
3. **build_report.sh**: Shell script that automates the entire workflow

## Requirements

- Python 3 with numpy, matplotlib, and pandas
- LaTeX installation (such as TeX Live or MiKTeX)
- Standard Unix-like shell environment

## How to Use

1. Clone or download this repository
2. Ensure you have the required dependencies installed
3. Run the build script:

```bash
./build_report.sh
```

4. The final report will be generated as `technical_report.pdf`

## Customization

- Edit `report_template.tex` to change the document structure and text
- Modify `generate_figures.py` to work with your own data and create different visualizations
- Adjust `build_report.sh` if you need additional processing steps

## Advantages of This Approach

1. **Reproducibility**: The entire report generation process is automated and can be version-controlled
2. **Separation of Concerns**: Content writing is separate from data processing and visualization
3. **Professional Quality**: LaTeX produces high-quality typesetting for scientific documents
4. **Efficiency**: Changes to data or analysis automatically propagate to the report

## Potential Extensions

1. Add support for bibliographies using BibTeX
2. Implement a Makefile for more complex dependency management
3. Create templates for different types of reports
4. Add version control integration

## License

This proof-of-concept is provided as-is, free to use and modify for your own projects.
