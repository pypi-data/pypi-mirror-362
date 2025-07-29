# dspacelogs: DSpace Log Analyzer

A simple library to analyze and visualize DSpace access logs.

---

## Installation

Install or upgrade to the latest version using pip:
```bash
pip install --upgrade dspacelogs
```
Quick Start Guide
This guide shows the simplest way to get your first results.

1. Create a Python Script
Create a new file, for example analyze.py.

2. Add Code and Edit Path
Copy the code below into your file. Remember to change the log_file_path to the actual path of your log file.

This example is a simplified version of the logic found in DSpace_run.py and uses the methods from the loganalyzer class.
```
from dspacelogs import loganalyzer

# Define the path to your log file
log_file_path = "C:/path/to/your/access.log"

# Create an analyzer instance
analyzer = loganalyzer(log_file_path=log_file_path)

# Load data and get a result
if analyzer.load_data():
    # Get and print the top 5 most frequent requests
    top_5_pages = analyzer.get_top_requests(n=5)
    print("Top 5 Pages:")
    print(top_5_pages)

    # You can also create a plot by uncommenting the next line
    # analyzer.plot_activity_by_minute()
```
3. Run Your Script
Open your terminal, navigate to your file's directory, and run it:

```bash
python analyze.py
```
You will see a table with the top 5 pages printed in your terminal.
