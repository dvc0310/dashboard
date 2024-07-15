import argparse
import os
from data_prep import DataPreparer

def parse_args():
    """Parse command line arguments for data preparation."""
    parser = argparse.ArgumentParser(description="Prepare data files for visualization.")
    parser.add_argument('--directory', type=str, default='datasets', help='Directory where all the data files are stored')
    parser.add_argument('--outage_file', type=str, required=True, help='Filename of the outage data file')
    parser.add_argument('--ppe_file', type=str, required=True, help='Filename of the property, plant, and equipment data file')
    return parser.parse_args()

def prepare_data(directory, outage_file, ppe_file):
    """Prepare the data using the DataPreparer module and save it to CSV."""
    try:
        dataprep = DataPreparer(folder=directory, outage_file_name=outage_file, financial_file_name=ppe_file,normalize=True)
        dataprep.save_to_csv(folder=directory)
        print(f"Data has been prepared and saved in {directory}.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Failed to find one or more specified files. Please check the file paths and names.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    args = parse_args()
    prepare_data(args.directory, args.outage_file, args.ppe_file)

if __name__ == '__main__':
    main()
