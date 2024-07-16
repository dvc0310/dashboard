import os
import pandas as pd
import numpy as np

def find_project_root(current_dir):
    marker = 'marker'  
    while current_dir != os.path.dirname(current_dir):  # Stop when the root directory is reached
        if marker in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise Exception("Project root with marker not found.")

def change_to_root():
    cwd = os.getcwd()
    print("Current working directory:", cwd)
    project_root = find_project_root(cwd)
    os.chdir(project_root)
    print("Changed to project root directory:", os.getcwd())