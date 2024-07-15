import pandas as pd
from data_prep import OutageDataProcessor, FinancialDataTransformer
import os

class DataPreparer:
    def __init__(self, outage_file_name, financial_file_name, start_year=2021, end_year=2023, folder='datasets', normalize=False):
        """
        Initializes DataPreparer with specific configurations for processing outage and financial data.

        Parameters:
            outage_file_name (str): The filename of the outage data CSV file.
            financial_file_name (str): The filename of the financial data CSV file.
            start_year (int, optional): The start year for filtering the data; defaults to 2021.
            end_year (int, optional): The end year for filtering the data; defaults to 2023.
            folder (str, optional): The directory where the data files are stored; defaults to 'datasets'.
            normalize (bool, optional): A flag to normalize the financial data during preparation; defaults to False.

        Initializes data processing objects for both outage and financial data and links the prepared data.
        """
        self.outage_processor = OutageDataProcessor(outage_file_name, start_year, end_year, folder=folder)
        self.financial_processor = FinancialDataTransformer(financial_file_name, folder=folder, normalize=normalize)
        self.link_data()

    def link_data(self):
        """
        Links prepared outage and financial data by 'Company', 'Year', and 'Quarter'.

        Fetches aggregated outage data and unpivoted financial data, then merges them on 'Company', 'Year', and 'Quarter'.
        The resulting DataFrame is cleaned to remove any rows with missing values and ensures all PP&E values are numeric.
        """
        print("Linking Data...")
        aggregated_outage_data = self.outage_processor.get_outage_frequency()
        unpivoted_finance = self.financial_processor.get_financial_data()
        self.linked_data = pd.merge(
            aggregated_outage_data,
            unpivoted_finance,
            on=['Company', 'Year', 'Quarter'],
            how='inner'
        )
        self.linked_data = self.linked_data.dropna(how='any')
        self.linked_data['PP&E'] = pd.to_numeric(self.linked_data['PP&E'], errors='coerce')
        self.linked_data = self.linked_data.dropna(subset=['PP&E'])

        print("Data linked successfully.")

    def get_data(self):
        """
        Returns the linked data after preparation.

        Returns:
            DataFrame: The fully prepared and linked data ready for analysis or export.
        """
        return self.linked_data

    def save_to_csv(self, folder='visualization', file_name='prepared_data.csv'):
        """
        Saves the linked data to a CSV file in a specified directory.

        Parameters:
            folder (str, optional): The directory to save the file; defaults to 'visualization'.
            file_name (str, optional): The name of the file to save; defaults to 'prepared_data.csv'.

        Ensures the target directory exists and writes the linked data to a CSV file, without including the index.
        """
        os.makedirs(folder, exist_ok=True)
        file_path = f"{folder}/{file_name}"
        self.linked_data.to_csv(file_path, index=False)
        print(f"Data saved successfully to {file_path}.")
