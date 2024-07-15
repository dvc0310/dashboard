
# Utility Functions Documentation (`read_util.py`)

## Overview

The `read_util.py` module contains utility functions used across the `data_prep` package for handling file encoding detection and data reading. These utilities simplify the process of loading data files by automating encoding detection and supporting multiple file formats.

## Table of Contents

1. [Overview](#overview)
2. [find_encoding Function](#find_encoding-function)
3. [read_file Function](#read_file-function)
4. [Usage](#usage)

## find_encoding Function

### Purpose

Determines the character encoding of a file by analyzing a sample of its contents.

### Parameters

- **fname** (str): Path to the file whose encoding needs to be determined.

### Returns

- **str**: The detected encoding of the file, or an error message if the file cannot be read or is not found.

### Error Handling

- Handles `FileNotFoundError` if the specified file does not exist.
- Handles `IOError` for issues related to file access.
- Handles general exceptions with a catch-all for unexpected errors.

### Example Usage

```python
encoding = find_encoding('path/to/data.csv')
```

## read_file Function

### Purpose

Reads a data file into a Pandas DataFrame, handling CSV, Excel, and potentially other formats while managing different encodings.

### Parameters

- **filepath** (str): Path to the file to be read.

### Returns

- **DataFrame**: A Pandas DataFrame containing the data from the file.
- Prints error messages directly if an issue arises during the file reading process.

### Supported File Formats

- **.csv**: Reads CSV files, automatically detecting encoding.
- **.xls, .xlsx**: Reads Excel files, using the `openpyxl` engine for `.xlsx`.

### Error Handling

- Handles `FileNotFoundError` for missing files.
- Handles `pd.errors.EmptyDataError` if the file is empty.
- Handles `pd.errors.ParserError` for formatting errors in the file.
- Handles general exceptions for other unexpected errors during file reading.

### Example Usage

```python
dataframe = read_file('path/to/data.csv')
```

## Usage

These utility functions are designed to be used by data processing classes within the `data_prep` package. They ensure that files are read correctly and work with a variety of common file issues, such as incorrect encodings or corrupt files.

