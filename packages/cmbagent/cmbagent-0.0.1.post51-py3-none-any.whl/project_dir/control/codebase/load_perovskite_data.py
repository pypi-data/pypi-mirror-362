# filename: codebase/load_perovskite_data.py
import pandas as pd
import json # Import json for more specific JSONDecodeError handling if needed

def load_perovskite_data(file_path):
    """
    Loads perovskite solar cell data from a JSON file into a pandas DataFrame.

    Args:
        file_path (str): The path to the JSON data file.

    Returns:
        pandas.DataFrame or None: A DataFrame containing the loaded data, 
                                   or None if an error occurs during loading.
    """
    try:
        # Attempt to load the JSON data directly into a pandas DataFrame
        # pandas read_json is generally robust and can handle lists of dictionaries,
        # where missing keys in some dictionaries will result in NaN values in the DataFrame.
        df = pd.read_json(file_path)
        print("Data loaded successfully from: " + file_path)
        # Example: Print the shape of the DataFrame to confirm loading
        print("Shape of the loaded DataFrame: " + str(df.shape))
        return df
    except FileNotFoundError:
        print("Error: The file was not found at the specified path: " + file_path)
        return None
    except ValueError as ve:
        # This can catch errors if JSON is malformed or if pandas has trouble parsing
        # specific structures that aren't straightforward lists of records.
        # For more specific JSON decoding errors, you might catch json.JSONDecodeError
        # if you were using the json module directly before pandas.
        print("Error: The JSON file is malformed or contains an invalid structure.")
        print("Pandas ValueError: " + str(ve))
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print("An unexpected error occurred while loading the data:")
        print(str(e))
        return None

if __name__ == '__main__':
    # Specify the path to the JSON data file
    data_path = "/Users/boris/CMBAgents/cmbagent_data/perovskite/device_attributes_combined.json"

    # Load the data using the defined function
    perovskite_df = load_perovskite_data(data_path)

    if perovskite_df is not None:
        # You can now work with the DataFrame, e.g., display its first few rows
        # print("\nFirst 5 rows of the DataFrame:")
        # print(perovskite_df.head())
        pass # Data is loaded, further processing can be done here.

    # Notice on how to use this script to load the data
    print("\n--- How to use this script to load the data ---")
    print("1. Ensure you have Python and the pandas library installed.")
    print("2. Save the code above as a Python file (e.g., 'load_data.py').")
    print("3. Modify the 'data_path' variable in the script to point to your JSON file location if it's different.")
    print("   Current path: " + data_path)
    print("4. Run the script from your terminal: python load_data.py")
    print("5. If successful, the 'perovskite_df' variable will contain the data as a pandas DataFrame.")
    print("   The script will print a success message and the shape of the DataFrame.")
    print("   If there are errors, an error message will be displayed.")
    print("-------------------------------------------------")
