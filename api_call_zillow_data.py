import pandas as pd
import numpy as np
import nasdaqdatalink
import zipfile
 
print(nasdaqdatalink.ApiConfig.api_key)
""""
zip_file_path     = nasdaqdatalink.export_table('ZILLOW/DATA', filename='ZILLOW_DATA.zip')
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall
        print(f"Successfully extracted all files from '{zip_file_path}' to working directory.")
except FileNotFoundError:
    print(f"Error: The file '{zip_file_path}' was not found.")
except zipfile.BadZipFile:
    print(f"Error: '{zip_file_path}' is not a valid ZIP file or is corrupted.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


zillow_data       = pd.read_csv('ZILLOW_DATA.csv', dtype={'indicator_id':'category', 'region_id':'category'}, parse_dates=['date'])
zillow_indicators = nasdaqdatalink.get_table('ZILLOW/INDICATORS',paginate=True)
zillow_regions    = nasdaqdatalink.get_table('ZILLOW/REGIONS',paginate=True)
"""