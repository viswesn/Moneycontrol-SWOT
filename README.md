# Moneycontrol-SWOT

We have set of Python scripts for various tasks related to stock data and analysis. Here's a brief summary of each script:

1. **get_stock_names.py:**
   - Purpose: Retrieves stock names and their corresponding Moneycontrol site links.
   - Output: Stores the information in a file named `stock.csv`.

2. **get_swot_details.py:**
   - Purpose: Reads `stock.csv` and calculates SWOT scores along with MC Essential scores for each stock.
   - Output: Creates a file named `swot_details.csv` containing the calculated scores.

3. **streamlit-swot.py:**
   - Purpose: Utilizes Python Streamlit to render a webpage for easy viewing of collected SWOT details.
   - Output: Provides a user-friendly interface to access the SWOT analysis data.

4. **MoneyControl.ipynb:**
   - Purpose: Designed to be used in Jupyter notebook, allowing real-time data science operations related to Moneycontrol SWOT data.

These scripts seem to form a cohesive workflow where you gather stock data, perform SWOT analysis, visualize the results using Streamlit, and have the flexibility for on-the-fly data science operations in Jupyter notebook using `MoneyControl.ipynb`.