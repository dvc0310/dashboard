## Environment Setup Guide for VSCode

### Step 1: Download and Install Visual Studio Code

Visual Studio Code is a powerful source code editor that runs on your desktop. It's available for Windows, macOS, and Linux.

- **Download**: Go to the [Visual Studio Code website](https://code.visualstudio.com/) and download the version appropriate for your operating system.
- **Install**: Follow the installation prompts to install VSCode on your machine.

### Step 2: Install Python

If Python is not already installed on your machine, you will need to install it.

- **Windows/macOS/Linux**:
  - Download Python from the [official Python website](https://www.python.org/downloads/).
  - Run the installer and follow the instructions. Make sure to check the box that says **Add Python to PATH** at the beginning of the installation.

### Step 3: Set Up Python in VSCode

Once VSCode and Python are installed, you'll need to configure VSCode to use the Python interpreter.

- **Open VSCode**.
- **Open the Command Palette** (Ctrl+Shift+P on Windows/Linux, Cmd+Shift+P on macOS).
- Type `Python: Select Interpreter`, and select the Python version you installed earlier.

### Step 4: Install VSCode Extensions for Python and Jupyter

VSCode supports Python development and Jupyter notebooks through extensions.

- **Python Extension**:
  - Open the Extensions view by clicking on the square icon on the sidebar or pressing Ctrl+Shift+X.
  - Search for `Python` and find the extension by Microsoft (officially recommended).
  - Click **Install**.
  
- **Jupyter Extension**:
  - In the same Extensions view, search for `Jupyter`.
  - Find the Jupyter extension by Microsoft.
  - Click **Install**.

These extensions provide rich support for Python, including features like IntelliSense, linting, debugging, code navigation, code formatting, Jupyter notebook support, PySpark, and more.

### Step 5: Create and Open a Jupyter Notebook

With the extensions installed, you can now create and open Jupyter notebooks directly in VSCode.

- **Create a New Notebook**:
  - Open the Command Palette again.
  - Type `Jupyter: Create New Blank Notebook`, and select the option.
  
- **Open an Existing Notebook**:
  - Navigate to the File Explorer inside VSCode (Ctrl+Shift+E).
  - Find a `.ipynb` file and click on it to open.

### Step 6: Install Required Python Packages

Ensure all necessary Python packages are installed for your project.

- **Open the Terminal** in VSCode (Ctrl+` or View -> Terminal).
- Install the required packages using pip. For example:
  ```bash
    pip install dash plotly pandas scipy statsmodels
  ```

### Step 7: Run Your Notebook

Once your notebook is open and your environment is set up:

- **Run Cells**: Click on the run button in the cell or use the shortcut (Ctrl+Enter).

---
