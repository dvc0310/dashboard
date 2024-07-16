import pandas as pd
import re
from .read_util import find_encoding, read_file
from config.config import company_aliases
import os
import numpy as np

class FinancialDataTransformer:
    """
    Processes financial data for analysis by loading, cleaning, transforming, and normalizing data from various file formats.

    Attributes:
        outage_file_path (str): Path to the financial data file.
        end_year (int): The last year in the data range for filtering.
        start_year (int): The first year in the data range for filtering.
        data (DataFrame or None): The processed financial data ready for analysis.
    """
    def __init__(self, financial_data_file_name, folder='datasets', normalize=False):
        """
        Initializes the FinancialDataProcessor with specified file, year range, and data folder.

        Parameters:
            financial_data_file_name (str): The name of the file containing the financial data.
            start_year (int): The starting year for data to include in processing.
            end_year (int): The ending year for data to include in processing.
            folder (str): The directory where financial data files are stored.
        """
        self.financial_data_file_path = f"{folder}/{financial_data_file_name}"
        self.finance_data = None
        self.is_data_prepared = False  
        self.normalize = normalize

    def get_financial_data(self):
        """
        Retrieves the prepared financial data. If the data is not already prepared, it triggers the preparation process.

        Ensures that financial data is loaded and prepared only once unless explicitly reset. This method is typically 
        called after setting new data parameters or when accessing the data for the first time.

        Returns:
            DataFrame: A pandas DataFrame containing the prepared financial data.
        """
        if not self.is_data_prepared:
            self.prepare_financial_data()
            self.is_data_prepared = True  # Set flag to True after data is prepared
        return self.finance_data
    
    def set_financial_data(self, financial_data_file_name, folder='datasets', normalize=False):
        """
        Sets the financial data file path and loads the data by initiating the preparation process. Allows the user 
        to change the source file and reinitialize the data processing.

        Parameters:
            financial_data_file_name (str): The name of the file containing the financial data.
            folder (str): The directory where the financial data file is stored, defaulting to 'datasets'.
            normalize (bool): Flag to indicate whether the data should be normalized during the preparation process.

        Effects:
            Resets the data preparation status and triggers reloading and re-preparing the data based on the new file path.
        """
        self.financial_data_file_path = f"{folder}/{financial_data_file_name}"
        self.normalize=normalize
        self.is_data_prepared = False
        self.finance_data = self.get_financial_data()

    def prepare_financial_data(self):
        """
        Conducts a series of data preparation steps on the financial data file specified in the object's attributes. 
        This method is designed to be run once unless explicitly re-invoked.

        Steps involved:
        - Reads data from the specified file path.
        - Loads raw data considering the file format.
        - Aligns and formats column headers.
        - Formats company names and removes unwanted columns.
        - Filters columns based on specific criteria.
        - Converts numeric columns from strings.
        - Unpivots the data for analysis.
        - Extracts and formats necessary columns like year and quarter.
        - Cleans and filters data based on company names using predefined aliases.

        Raises:
            FileNotFoundError: If the specified file cannot be found at the given path.
            ValueError: For various errors like unsupported file formats or parsing issues.
            UnicodeDecodeError: For encoding issues in the file.
            Exception: Catches and logs unexpected errors during data processing.
        """
        print('Reading finance data from:', self.financial_data_file_path)
        self.finance_data = read_file(self.financial_data_file_path)
        self.__load_raw_data()
        self.__align_data()
        self.__format_company_column()
        self.__filter_financial_columns()
        self.__convert_columns_to_numeric()
        self.__unpivot_data(['Company'], normalize=self.normalize)
        self.__extract_and_format_columns()
        self.__filter_and_clean_company_data()

    def __load_raw_data(self):
        """
        Loads raw data from a specified file path into a pandas DataFrame. The method supports both CSV and Excel file formats.
        """
        file_extension = os.path.splitext(self.financial_data_file_path)[1]
        try:
            if file_extension == '.csv':
                encoding = find_encoding(self.financial_data_file_path)
                self.finance_data = pd.read_csv(self.financial_data_file_path, header=None, encoding=encoding)
                self.finance_data = self.finance_data.applymap(lambda x: np.nan if isinstance(x, str) and x.startswith('#') else x)
            elif file_extension in ['.xls', '.xlsx']:
                self.finance_data = pd.read_excel(self.financial_data_file_path, header=None, engine='openpyxl')
            else:
                raise ValueError("Unsupported file format: {}".format(file_extension))
        except pd.errors.EmptyDataError:
            raise ValueError("No data: The file is empty.")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing the file: {e}")
        except FileNotFoundError:
            raise ValueError(f"File not found: {self.financial_data_file_path}")
        except UnicodeDecodeError:
            raise ValueError(f"Encoding error in the file: {self.financial_data_file_path}")
        except Exception as e:
            raise SystemError(f"An unexpected error occurred: {e}")

    def __align_data(self):
        """
        Aligns and formats the column headers of the financial data based on specific criteria.

        The method contains two nested functions:
        - align_column_headers: Adjusts column names directly from the first row if there are missing or `NaN` values.
        - check_column_pattern: Validates if any of the column names match a specific pattern (e.g., 'CQ1YYYY' for quarters).

        Steps performed:
        1. Checks if the 'Company' column exists and if any column matches the quarter-year format.
        2. If checks fail, it attempts to clean the data by dropping completely empty rows and resetting column names from the first data row.
        3. The column headers are then aligned twice to ensure that adjustments take hold, especially in cases where initial headers are incorrect or misplaced.
        4. Continues until the headers are correctly set or until all predefined shifts are attempted.
        """
        def align_column_headers():
            """ Helper function to replace NaN or incorrect column headers from the first row of the DataFrame. """
            result = []
            for i, col in enumerate(self.finance_data.iloc[0]):
                if not pd.isna(col):
                    result.append(col)
                else:
                    result.append(self.finance_data.columns[i])
            self.finance_data.columns = result
    
        def check_column_pattern(columns):
            """ Checks if any column names fit a specific quarter-year format, returns True if at least one matches. """
            pattern = re.compile(r'CQ[1-4]\d{4}')
            return any(re.match(pattern, str(col)) for col in columns)

        if 'Company' not in self.finance_data.columns or not check_column_pattern(self.finance_data.columns):
            print("The data file is missing the 'Company' column or does not have any quarter-year format columns; attempting to clean data...")

            # Drops all rows with all null values
            self.finance_data.dropna(how='all', inplace=True)

            # Set the column names to be the same as the ones in the first row
            self.finance_data.columns = self.finance_data.iloc[0]
            for _ in range(2):
                align_column_headers()
                self.finance_data= self.finance_data[1:]
                self.finance_data.reset_index(drop=True, inplace=True)
                done_shifting = 'SP_ENTITY_NAME' in self.finance_data.columns and pd.notna(self.finance_data.iat[0,0])
                if done_shifting:
                    break

    def __format_company_column(self):
        """
        Renames and formats the 'Company' column in the financial data.
        """
        self.finance_data.rename(columns={'SP_ENTITY_NAME':'Company'},inplace=True)
        if 'SP_ENTITY_ID' in self.finance_data.columns:
            self.finance_data.drop('SP_ENTITY_ID', axis=1, inplace=True)
            print(f"Column 'SP_ENTITY_ID' removed successfully.")

        self.finance_data['Company'] = self.finance_data['Company'].str.replace(r"\s*\([^)]+\)", "", regex=True)
        self.finance_data['Company'] = self.finance_data['Company'].str.strip()
        
    def __filter_financial_columns(self):
        """
        Filters the columns in the financial data to include only the 'Company' column and those matching a specific quarterly data pattern.
        """
        pattern = re.compile(r'^CQ\d{1,2}\d{4}$')

        columns_to_keep = [col for col in self.finance_data.columns if col == 'Company' or pattern.match(col)]
        if len(columns_to_keep) <= 1:
            raise ValueError("The Financial Data is in an invalid format.")
        
        self.finance_data = self.finance_data[columns_to_keep]
 
    def __convert_columns_to_numeric(self):
        """Converts non-'Company' columns in financial data to numeric types, handling non-numeric errors."""
        for col in self.finance_data.columns:
            if col != 'Company':
                self.finance_data[col] = pd.to_numeric(self.finance_data[col], errors='coerce')


    def __unpivot_data(self, id_vars, var_name='Quarter', value_name='PP&E',normalize=True):
        """Converts wide data to long format and scales specific variables if necessary."""
        self.finance_data = self.finance_data.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)
        if normalize:
            self.finance_data[value_name] /= 1000000000  # Normalize large values for easier handling
        print("Data successfully unpivoted and normalized.")

    def __extract_and_format_columns(self):
        """Extracts year and quarter from the 'Quarter' column and formats them."""
        if 'Quarter' in self.finance_data.columns:
            self.finance_data['Year'] = self.finance_data['Quarter'].str[-4:].astype(int)
            self.finance_data['Quarter'] = self.finance_data['Quarter'].str[1:3].astype(str)
            print("Quarter and Year columns created successfully.")

    def __filter_and_clean_company_data(self):
        """Filters finance data based on company aliases and cleans the 'Company' column."""
        self.finance_data = self.finance_data[self.finance_data['Company'].isin(company_aliases.values())]
        self.finance_data['Company'] = self.finance_data['Company'].str.strip()
        print("Finance data filtered and company names cleaned successfully.")

