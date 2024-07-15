# Dash Web Application Documentation


## Overview


The Dash web application provides two primary key functions. It:

- **Links Outage Data and Financial Data**: Integrates outage data and financial data from S&P Capital IQ, and processes the linked data through custom modules.
- **Visualizes Processed Data**: Sets up an interactive web-based dashboard and automatically opens this dashboard in a user's default web browser.


## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Obtaining S&P Financial Data](#obtaining-sp-financial-data)
4. [Obtaining NORS Data](#obtaining-NORS-data)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Code Documentation](#code-documentation)

## Prerequisites

Before running this application, the following dependencies must be installed:

- Dash
- Plotly
- Pandas
- scipy
- statsmodels
- faker

These Python packages can be installed via pip:

```bash
pip install dash plotly pandas scipy statsmodels faker
```

Ensure that you have the following project-specific packages:

- `frontend`: Handles the creation of the Dash layout and the registration of callbacks.
- `visualization`: Contains the `PlotlyVisualizer` class for creating visualizations.
- `data_prep`: Manages the preparation and cleaning of data.

Additionally, financial data from the S&P Capital IQ Pro database is required. See the next section for detailed steps on how to obtain this data.

## Obtaining S&P Financial Data

Follow the steps provided [here.](docs/S&P.md)

Note that the file will have to look something like this:
![alt text](image-1.png)

## Obtaining NORS Data

You can obtain the NORS dataset only if you're affiliated with the FCC. For testing purposes, you can generate fake outage data in the `fake_data_generator.ipynb` file in the datasets folder. If you do have the real NORS outage data, place the csv file in the `datasets` directory.

![alt text](image-3.png)


## Installation

1. **Download or Clone the Repository**:
   Clone the source code from your repository or download the project folder containing all the necessary files and packages.

2. **Environment Setup**:
   Set up a Python environment and install the required dependencies as listed in the prerequisites. If you're not familiar with setting up a Python environment, click [here](docs/environment.md) for a more detailed guide.

## Usage

This section describes how to use the Dash web application and the standalone data preprocessor.

### Running the Data Preprocessor

The data preprocessor can be run independently to prepare your data before visualization. This can be especially useful if you choose to visualize the data through a more user friendly data visualization tool such as **PowerBI** or **Tableau**. To execute the data preprocessor, provide the necessary file specifications:

```bash
python prepare_data.py --directory "datasets" --outage_file "outage_data.csv" --ppe_file "ppe.xlsx"
```

### Running the Dashboard

To launch the interactive dashboard, you must specify the paths to the outage and PP&E data files. You can do this via command-line arguments. Use the following command to run the dashboard:

```bash
python dashboard.py --directory "datasets" --outage_file "outage_data.csv" --ppe_file "ppe.xlsx"
```

If you don't want to use the terminal directly, you can use these commands on a Jupyter Notebook file. Open `app.ipynb` and run the cell that contains the data preparation and dashboard commands.

### Tips for Running Scripts

- Ensure that Python and all required libraries (as listed in the Prerequisites section) are properly installed in your environment.
- Verify that the specified data files exist in your directory before running the commands to avoid errors.
- Adjust the directory path and filenames based on your actual file locations and names.


---

## Code Documentation

- **`frontend`**: Package defining the Dash layout and registering callbacks. [More Info](frontend/README.md)
- **`visualization`**: Package for visualizing the prepared data. [More Info](visualization/README.md)
- **`data_prep`**: Package for preparing and cleaning data. [More Info](data_prep/README.md)

---
