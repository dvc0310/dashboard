import pandas as pd
import logging
from .read_util import find_encoding
from config import company_aliases

import pandas as pd
import logging
from .read_util import find_encoding
from config import company_aliases

class OutageDataProcessor:
    def __init__(self, outage_file_name, start_year, end_year, folder="datasets"):
        """
        Initializes the OutageDataProcessor with specified file, year range, and storage folder.

        Parameters:
            outage_file_name (str): The name of the outage data file.
            start_year (int): The starting year for filtering the data.
            end_year (int): The ending year for filtering the data.
            folder (str): The directory where the outage data file is stored.

        Initializes logging and starts the data loading and processing workflow.
        """
        self.outage_file_path = f"{folder}/{outage_file_name}"
        self.start_year = start_year
        self.end_year = end_year
        self.data = None

        logging.info(f"Initialized with year range {self.start_year} to {self.end_year}.")
        self.load_and_process_outage_data()

    def load_and_process_outage_data(self):
        """
        Loads and processes outage data from a specified file using defined columns and filters data based on years and status.

        Filters include:
        - Company
        - Incident date and time
        - Outage report status
        """
        use_columns = ['u_company', 'u_incident_date_time', 'u_outage_report_status']
        filtered_chunks = self.__load_csv_in_chunks_and_filter(chunk_size=10000, use_columns=use_columns)
        self.data = self.__combine_and_process_chunks(filtered_chunks)

    def get_outage_frequency(self):
        """
        Aggregates the preprocessed data by company, year, and quarter, and counts the number of outages.

        Returns:
            DataFrame: A DataFrame with the count of outages grouped by company, year, and quarter.
            None: If the data is empty or not properly loaded, returns None.
        """
        if self.data is not None and not self.data.empty:
            return self.__aggregate_outage_data()
        else:
            logging.warning("Data is empty or not loaded properly. Please check the data loading process.")
            return None

    def __combine_and_process_chunks(self, chunks):
        """
        Combines filtered data chunks into a single DataFrame and extracts year and quarter from the incident dates.
        """
        def extract_year_and_quarter(data):
            data['Year'] = pd.to_datetime(data['u_incident_date_time']).dt.year.astype(int)
            data['Quarter'] = 'Q' + pd.to_datetime(data['u_incident_date_time']).dt.quarter.astype(str)

        data = pd.concat(chunks, ignore_index=True)
        data.rename(columns={'u_company': 'Company'}, inplace=True)
        extract_year_and_quarter(data)  

        return data

    def __filter_chunk_by_criteria(self, chunk):
        """
        Filters each data chunk by specified criteria including year range, report status, and company validity.
        """
        def convert_column_to_datetime(column):
            for fmt in ["%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M", "%m/%d/%Y", "%Y-%m-%d"]:
                try:
                    return pd.to_datetime(column, format=fmt, errors='raise')
                except ValueError:
                    continue
            return pd.to_datetime(column, errors='coerce')
        
        chunk['u_incident_date_time'] = convert_column_to_datetime(chunk['u_incident_date_time'])
        chunk['u_company'] = chunk['u_company'].str.strip().map(company_aliases)

        valid_years = chunk['u_incident_date_time'].dt.year.between(self.start_year, self.end_year)
        is_final = chunk['u_outage_report_status'] == 'Final'
        company_is_valid = chunk['u_company'].isin(company_aliases.values())

        return chunk[valid_years & is_final & company_is_valid]

    def __load_csv_in_chunks_and_filter(self, chunk_size, use_columns):
        """
        Reads the outage data file in chunks, applying filters to each chunk.
        """
        chunks = []
        for chunk in pd.read_csv(self.outage_file_path, encoding=find_encoding(self.outage_file_path), usecols=use_columns, chunksize=chunk_size):
            chunks.append(self.__filter_chunk_by_criteria(chunk))
        return chunks

    def __aggregate_outage_data(self):
        """
        Aggregates the data by 'Company', 'Year', and 'Quarter' and computes the count of records for each group.
        """
        return self.data.groupby(['Company', 'Year', 'Quarter']).size().reset_index(name='Count')
