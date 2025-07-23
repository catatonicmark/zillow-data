import pandas as pd
import nasdaqdatalink
import zipfile
import pymssql
import hashlib
import csv

NASDAQ_DATA_LINK_API_KEY =   nasdaqdatalink.read_key('/Users/tylerpruitt/Desktop/ZILLOW/data_link_apikey.rtf')

def define_api_key():
    nasdaqdatalink.ApiConfig.api_key = nasdaqdatalink.read_key('/Users/tylerpruitt/Desktop/ZILLOW/data_link_apikey.rtf')

def connect_to_sql_server():
    connection = pd.read_csv('/Users/tylerpruitt/Desktop/ZILLOW/account_info.csv')
    connection = connection.to_dict('list')
    con=pymssql.connect(connection['host'][0], connection['username'][0], connection['password'][0], connection['db'][0])
    cursor=con.cursor()
    return cursor


def extract_from_NASDAQ(big_data_table: str): 
    edited_filename = big_data_table.replace('/', '_')
    nasdaqdatalink.export_table(big_data_table, filename=f"{edited_filename}.zip", qopts={'export': 'true'})
    try:
        with zipfile.ZipFile(f'/Users/tylerpruitt/Desktop/ZILLOW/{edited_filename}', 'r') as zip_ref:
            zip_ref.extractall
            print(f"Successfully extracted all files from {edited_filename}.zip to working directory.")
    except FileNotFoundError:
        print(f"Error: The file {edited_filename}.zip was not found.")
    except zipfile.BadZipFile:
        print(f"Error: {edited_filename}.zip is not a valid ZIP file or is corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    data = pd.read_csv(f'{edited_filename}.csv', dtype={'indicator_id':'category', 'region_id':'category'}, parse_dates=['date'])
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
        return df.astype(str).agg('||'.join, axis=1).apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    NASDAQ_hashes = row_hash(NASDAQ_data)
    sql_hashes = row_hash(sql_data)
    new_rows = NASDAQ_data[~NASDAQ_hashes.isin(sql_hashes)]
    return new_rows

def clean_file(df: pd.DataFrame):
    df = df.replace({",":""}, regex=True)
    return df

print("API Key defined")
#zillow_data_NQ = extract_from_NASDAQ('ZILLOW/DATA')
#zillow_data_NQ = pd.read_csv('/Users/tylerpruitt/Desktop/ZILLOW/ZILLOW_DATA.csv', dtype={'indicator_id':'category','region_id':'category'},parse_dates=['date'])
print("Data extracted from NASDAQ")
cursor = connect_to_sql_server()
print("Connected to SQL Server")
zillow_data_SQL = read_data_from_SQL('[zillow-data-all].[dbo].[ZILLOW_DATA]', cursor)
print("Data received from SQL Server")
new_rows = compare_data(zillow_data_NQ, zillow_data_SQL)
print("Differences calculated")
print(new_rows)
