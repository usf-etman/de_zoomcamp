#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os

parser = argparse.ArgumentParser(description='Download CSV Data & Ingest it to Postgres')
parser.add_argument('--user', help='user for postgres')
parser.add_argument('--password', help='password for postgres')
parser.add_argument('--host', help='hostname for postgres')
parser.add_argument('--port', help='port for postgres')
parser.add_argument('--db', help='database name to insert into')
parser.add_argument('--table_name', help='table name to insert into')
parser.add_argument('--url', help='URL to download data')

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    while True:
        t_start = time()
        
        try:
            df = next(df_iter)
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
        
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        
        df.to_sql(con=engine, name=table_name, if_exists='append')
        
        t_end = time()
        print("Inserted Another chunk... Took %.3f seconds" % (t_end - t_start))

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)