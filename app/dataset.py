import os
from glob import glob
import pandas as pd

columns = [
    'id',
    'latitude',
    'longitude',
    'resale',
    'floor',
    'number_of_floors',
    'number_of_rooms',
    'area_total',
    'area_kitchen',
    'condition',
    'house_type',
    'balcony',
    'parking',
    'price_usd'
]


def get_X_y(csv_dir, last_files_count=10):
    csf_files_pattern = os.path.join(csv_dir, 'onliner_minsk_*.csv')
    print(csf_files_pattern)
    files = glob(csf_files_pattern)
    files = sorted(files, reverse=True)[:last_files_count]
    dfs_to_concat = []
    for file in files:
        df_file = pd.read_csv(file, sep=';', usecols=columns, encoding='utf-8')
        dfs_to_concat.append(df_file)

    df = pd.concat(dfs_to_concat)
    df = df.drop_duplicates('id').drop(columns=['id'])
    X, y = df.drop(columns=['price_usd']), df['price_usd']
    return X, y
