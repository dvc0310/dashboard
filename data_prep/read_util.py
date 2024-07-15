import chardet
import os
import pandas as pd
def find_encoding(fname):
    try:
        with open(fname, 'rb') as f:
            result = chardet.detect(f.read(100000))  # Read the first 100000 bytes to detect encoding
            return result['encoding']
    except FileNotFoundError:
        return "Error: File not found."
    except IOError as e:
        return f"Error: Unable to read file. {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred. {e}"
    
def read_file( filepath):
    try:
        file_extension = os.path.splitext(filepath)[1]
        if file_extension == '.csv':
            return pd.read_csv(filepath, encoding=find_encoding(filepath))
        elif file_extension in ['.xls', '.xlsx']:
            return pd.read_excel(filepath, header=None, engine='openpyxl')
        else:
            raise ValueError("Unsupported file format")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except pd.errors.EmptyDataError:
        print(f"No data: {filepath} is empty")
    except pd.errors.ParserError:
        print(f"Parsing error: {filepath} is malformed")
    except Exception as e:
        print(f"An error occurred while reading {filepath}: {e}")