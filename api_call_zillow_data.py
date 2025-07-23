import pandas as pd
import nasdaqdatalink
import zipfile
import pymssql
import hashlib

def define_api_key():
    nasdaqdatalink.ApiConfig.api_key = nasdaqdatalink.read_key()

def connect_to_sql_server():
    connection = pd.read_csv('account_info.csv')
    con=pymssql.connect(connection['host'],connection['username'],connection['password'],connection['db'])
    cursor=con.cursor()
    return cursor


def extract_from_NASDAQ(big_data_table: str): 
    filename = big_data_table.replace('/', '_')
    nasdaqdatalink.export_table(big_data_table, f"{filename}.zip")
    try:
        with zipfile.ZipFile(filename + ".zip", 'r') as zip_ref:
            zip_ref.extractall
            print(f"Successfully extracted all files from {filename}.zip to working directory.")
    except FileNotFoundError:
        print(f"Error: The file {filename}.zip was not found.")
    except zipfile.BadZipFile:
        print(f"Error: {filename}.zip is not a valid ZIP file or is corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    data = pd.read_csv(f'{filename}.csv', dtype={'indicator_id':'category', 'region_id':'category'}, parse_dates=['date'])
    return data

def read_data_from_SQL(table_name: str, cursor):
    sql_query = f"SELECT * FROM {table_name}"
    sql_data = pd.read_sql(sql_query, cursor)
    return sql_data

def get_from_NASDAQ(table_code: str):
    data = nasdaqdatalink.get_table(table_code,paginate=True)
    return data

def compare_data(NASDAQ_data: pd.DataFrame, sql_data: pd.DataFrame):
    def row_hash(df):
        return df.astype(str).agg('||'.join, axis=1.apply(lambda x: hashlib.md5(x.encode()).hexdigest()))
    NASDAQ_hashes = row_hash(NASDAQ_data)
    sql_hashes = row_hash(sql_data)
    new_rows = NASDAQ_data[~NASDAQ_hashes.isin(sql_hashes)]
    return new_rows