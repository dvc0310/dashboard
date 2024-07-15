import argparse
import os
from dash import Dash
from frontend import create_layout, register_callbacks
from visualization import PlotlyVisualizer
from data_prep import DataPreparer
import webbrowser
from threading import Timer

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Run the Dash web application for visualizing data.")
    parser.add_argument('--directory', type=str, default='datasets', help='Directory where data files are stored')
    parser.add_argument('--outage_file', type=str, required=True, help='Filename of the outage data file')
    parser.add_argument('--ppe_file', type=str, required=True, help='Filename of the property, plant, and equipment data file')
    
    return parser.parse_args()

def main():
    args = parse_args()

    app = Dash(__name__, suppress_callback_exceptions=True)

    # Build paths to the data files
    outage_file_path = os.path.join(args.directory, args.outage_file)
    ppe_file_path = os.path.join(args.directory, args.ppe_file)

    try:
        # Check if the specified files exist
        if not os.path.exists(outage_file_path) or not os.path.exists(ppe_file_path):
            raise FileNotFoundError("One or more specified data files are missing.")

        # Data preparation using the specified files
        dataprep = DataPreparer(folder=args.directory, outage_file_name=args.outage_file, financial_file_name=args.ppe_file,normalize=True)
        dataprep.save_to_csv(folder=args.directory)
        prepared_data_file = 'prepared_data.csv'
        visualizer = PlotlyVisualizer(filename=prepared_data_file, directory=args.directory)
        app.layout = create_layout(visualizer)
        register_callbacks(app, visualizer)

        def open_browser():
            webbrowser.open_new("http://127.0.0.1:8050/")

        Timer(1, open_browser).start()
        app.run_server(debug=False)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Failed to find one or more specified files. Please check the file paths and names.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
