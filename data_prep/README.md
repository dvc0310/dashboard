
# Data Preparation Package Documentation

## Overview

The `data_prep` package is designed to handle the preparation and transformation of data for a Dash web application. This package includes classes and utilities for processing outage data, financial data, and linking these datasets for visualization purposes.

## Table of Contents

1. [Overview](#overview)
2. [Components](#components)
    - [OutageDataProcessor](docs/OutageDataProcessor.md)
    - [FinancialDataTransformer](docs/FinancialDataTransformer.md)
    - [Utility Functions](docs/read_util.md)
3. [DataPreparer Class](#datapreparer-class)
4. [Usage](#usage)

## Components

This package comprises several key components that manage different aspects of data handling:

- **OutageDataProcessor**: Manages the processing of outage data, including filtering and aggregating data based on specified criteria. [More Details](docs/OutageDataProcessor.md)
- **FinancialDataTransformer**: Handles the transformation of financial data related to property, plant, and equipment (PP&E). [More Details](docs/FinancialDataTransformer.md)
- **Utility Functions**: A collection of utility functions that assist in data manipulation and transformation tasks. [More Details](docs/read_util.md)

## DataPreparer Class

### Overview

The `DataPreparer` class orchestrates the preparation of data by utilizing the `OutageDataProcessor` and `FinancialDataTransformer` to process and link data effectively. This class ensures that the data from different sources is merged based on common identifiers such as 'Company', 'Year', and 'Quarter'.

### Functions

- **`__init__()`**: Initializes the data processors and sets up file paths and parameters for data processing.
- **`link_data()`**: Links the processed data from different sources into a single dataset.
- **`get_data()`**: Retrieves the fully prepared and linked dataset.
- **`save_to_csv()`**: Saves the linked dataset to a CSV file for further use or visualization.

## Usage

The `DataPreparer` class is utilized within the data preparation stage of the application lifecycle. It is typically called before visualization tasks to ensure that the data is properly prepared and saved.
