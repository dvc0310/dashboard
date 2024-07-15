# Callbacks Documentation for the Frontend Package

## Overview

`callbacks.py` manages the interactivity of the Dash web application by defining and registering callback functions. These functions update the application's visualizations based on user inputs, such as selections of companies, date ranges, and visualization preferences.

## Table of Contents

1. [Overview](#overview)
2. [Callback Functions](#callback-functions)
    - [Update Graph Tab 1](#update-graph-tab-1)
    - [Update Graph Tab 2](#update-graph-tab-2)
    - [Update Graph Tab 3](#update-graph-tab-3)
    - [Display Prediction Interval Options](#display-prediction-interval-options)
3. [Usage](#usage)

## Callback Functions

### Update Graph Tab 1

**Function**: `update_graph_tab1`

- **Purpose**: Updates the visualization in the first tab based on selected companies, interval preferences, view mode, and selected date range.
- **Inputs**:
  - `company-dropdown-tab1`: Selected companies from a dropdown.
  - `checklist`: Determines whether to enable intervals.
  - `view-toggle`: Switch between 'Granular' and 'Aggregated' views.
  - `date-picker-range1`: Start and end dates from the date picker.
- **Output**:
  - `graph-tab1`: Updates the figure in the first tab with either granular or aggregated outage data visualization.
- **Details**:
  - In 'Granular' mode, the function calls `plot_granular_outage_vs_ppe`.
  - In 'Aggregated' mode, it calls `plot_average_outage_vs_ppe`.

### Update Graph Tab 2

**Function**: `update_graph_tab2`

- **Purpose**: Updates the line chart visualization in the second tab based on selected companies and date range.
- **Inputs**:
  - `company-dropdown-tab2`: Selected companies.
  - `date-picker-range2`: Start and end dates.
- **Output**:
  - `graph-tab2`: Renders an updated line chart showing outage over time for selected companies.

### Update Graph Tab 3

**Function**: `update_graph_tab3`

- **Purpose**: Refreshes the boxplot visualization in the third tab, incorporating options for including grand total data.
- **Inputs**:
  - `company-dropdown-tab3`: Selected companies.
  - `grand-total-checklist`: Checkbox to include grand total data in the visualization.
  - `date-picker-range3`: Start and end dates.
- **Output**:
  - `graph-tab3`: Updates the box plot to reflect the current selections and settings.


## Usage

These callbacks are registered within the Dash application context and are triggered by user interactions with the web interface. Each callback listens for changes in specific components and updates parts of the application accordingly. 
