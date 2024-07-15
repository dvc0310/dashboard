import pandas as pd
import re
from .read_util import find_encoding, read_file
from config import company_aliases
import os
import numpy as np

class FinancialDataTransformer:
    def __init__(self, financial_data_file_name, folder='datasets'):
        """
        Initialize the FinancialDataTransformer with the paths to a Finance data CSV file and a mapper CSV file.
        """
        self.financial_data_file_path = f"{folder}/{financial_data_file_name}"
        self.finance_data = None
        self.is_data_prepared = False  
    

    def get_financial_data(self):
        """
        Return the current state of the Finance data. Load and prepare data if not already done.
        """
        if not self.is_data_prepared:
            self.__load_financial_data()
            self.__remove_column('SP_ENTITY_ID')
            self.__unpivot_data(['Company'])
            self.is_data_prepared = True  # Set flag to True after data is prepared
        return self.finance_data
    
    def set_financial_data(self, financial_data_file_name, folder='datasets'):
        self.financial_data_file_path = f"{folder}/{financial_data_file_name}"
        self.is_data_prepared = False 
        self.finance_data = self.get_financial_data()

    def __load_financial_data(self):
        """
        Load Financial data from the CSV file and load the company name mapper file.
        This method ensures all necessary columns are present and properly named.
        """
        print('Reading finance data from:', self.financial_data_file_path)
        self.finance_data = read_file(self.financial_data_file_path)
        self.__load_cleaned_data()

        self.__validate_column_names()
        self.__convert_string_to_numeric()

    def __load_cleaned_data(self):
        """
        Load data from a file (CSV or Excel), clean it by renaming columns, removing unwanted data, and adjusting headers.
        """
        self.__load_and_set_unprocessed_data()
        self.__process_and_clean_data()

    def __shift_column_names(self):
        self.finance_data.columns = [col if not pd.isna(col) else self.finance_data.columns[i] for i, col in enumerate(self.finance_data.iloc[0])]
    
    def __load_and_set_unprocessed_data(self):
        file_extension = os.path.splitext(self.financial_data_file_path)[1]
        if file_extension == '.csv':
            try:
                self.finance_data = pd.read_csv(self.financial_data_file_path, header=None, encoding=find_encoding(self.financial_data_file_path))
                self.finance_data = self.finance_data.applymap(lambda x: np.nan if isinstance(x, str) and x.startswith('#') else x)

            except Exception as e:
                raise ValueError(f"Error reading the CSV file: {e}")

        elif file_extension in ['.xls', '.xlsx']:
            self.finance_data= pd.read_excel(self.financial_data_file_path, header=None, engine='openpyxl')
        else:
            raise ValueError("Unsupported file format")
    
    def __process_and_clean_data(self):
        if 'Company' not in self.finance_data.columns:
            print("The data file is missing the 'Company' column; attempting to clean data...")

            # Drops all rows with all null values
            self.finance_data.dropna(how='all', inplace=True)

            # Set the column names to be the same as the ones in the first row
            self.finance_data.columns = self.finance_data.iloc[0]
            for _ in range(2):
                self.__shift_column_names()
                self.finance_data= self.finance_data[1:]
                self.finance_data.reset_index(drop=True, inplace=True)
                if 'Company' in self.finance_data.columns or ('SP_ENTITY_NAME' in self.finance_data.columns and pd.notna(self.finance_data.iat[0,0])):
                    break

        self.finance_data.rename(columns={'SP_ENTITY_NAME':'Company'},inplace=True)
        if 'SP_ENTITY_ID' in self.finance_data.columns:
            self.finance_data.drop('SP_ENTITY_ID', axis=1, inplace=True)

        self.__remove_parantheses()

    def __remove_parantheses(self):
        self.finance_data['Company'] = self.finance_data['Company'].str.replace(r"\s*\([^)]+\)", "", regex=True)
        self.finance_data['Company'] = self.finance_data['Company'].str.strip()

    def __split_quarter_year(self):
        """
        Split the 'Quarter' column into separate 'Quarter' and 'Year' columns in the Finance data.
        """
        if 'Quarter' in self.finance_data.columns:
            self.finance_data['Year'] = self.finance_data['Quarter'].str[-4:]
            self.finance_data['Quarter'] = self.finance_data['Quarter'].str[1:3]
            print("Quarter and Year columns created successfully.")
    
    def __filter_by_company(self):
        """
        Filter the Finance data to only include rows where the company name is in the provided list of companies to include.
        """
        self.finance_data = self.finance_data[self.finance_data['Company'].isin(company_aliases.values())]
        print("Finance data filtered successfully.")

    def __validate_column_names(self):
        """
        Validate that column names match the expected 'CQ{quarter_number}{year}' format.
        """
        pattern = re.compile(r'^CQ\d{1,2}\d{4}$')

        columns_to_keep = [col for col in self.finance_data.columns if col == 'Company' or pattern.match(col)]
        if len(columns_to_keep) <= 1:
            raise ValueError("The Financial Data is in an invalid format.")
        
        self.finance_data = self.finance_data[columns_to_keep]


    def __convert_string_to_numeric(self):
        for col in self.finance_data.columns:
            if col != 'Company':
                self.finance_data[col] = pd.to_numeric(self.finance_data[col], errors='coerce')


    def __remove_column(self, column_name):
        """
        Remove a specified column from the Finance data.
        """
        if column_name in self.finance_data.columns:
            self.finance_data.drop(column_name, axis=1, inplace=True)
            print(f"Column '{column_name}' removed successfully.")

    def __unpivot_data(self, id_vars, var_name='Quarter', value_name='PP&E'):
        """
        Unpivot the Finance dataframe, keeping 'id_vars' as identifier variables.
        """
        self.finance_data = self.finance_data.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)
        if value_name == 'PP&E':
            self.finance_data[value_name] /= 1000000000
        self.__split_quarter_year()
        self.__filter_by_company()

        self.finance_data['Year'] = self.finance_data['Year'].astype(int)
        self.finance_data['Quarter'] = self.finance_data['Quarter'].astype(str)
        self.finance_data['Company'] = self.finance_data['Company'].astype(str)
        self.finance_data['Company'] = self.finance_data['Company'].str.strip()

        print("Finance data unpivoted successfully.")