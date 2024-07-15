import pandas as pd
from data_prep import OutageDataProcessor, FinancialDataTransformer
import os 

class DataPreparer:
    def __init__(self, outage_file_name, financial_file_name, start_year=2021, end_year=2023, folder='datasets'):
        """
        Initialize the DataLinker with the paths to the outage data and Financial data CSV files.
        """
        self.outage_processor = OutageDataProcessor(outage_file_name, start_year, end_year, folder=folder)
        self.financial_processor = FinancialDataTransformer(financial_file_name, folder=folder)
        self.link_data()
        
    
    def link_data(self):
        """
        Link the prepared outage and PPE data on 'Company', 'Year', and 'Quarter'.
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
        Return the linked data.
        """
        return self.linked_data
    
    def save_to_csv(self, folder='visualization',file_name='prepared_data.csv'):
        """
        Save the data to a csv file.
        """       
        os.makedirs(folder, exist_ok=True)

        file = f"{folder}/{file_name}"

        self.linked_data.to_csv(file, index=False)

