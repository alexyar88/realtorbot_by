import requests
import time
import csv
import os
import joblib
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

from custom_transformer import CustomTransformer
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer, ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from lightgbm.sklearn import LGBMRegressor
from xgboost.sklearn import XGBRegressor

import numpy as np
import pandas as pd


from flask import Blueprint, render_template, request, jsonify


csv_path = str(Path(__file__).parent.absolute()) + '/../data/'
model_path = str(Path(__file__).parent.absolute()) + '/../ml_models/'

is_docker = os.environ.get('IS_DOCKER', False)
if is_docker:
    csv_path = '/mounted/data/'
    model_path = '/mounted/models/'


train_model = Blueprint('train_model', __name__)

@train_model.route('/train-model-and-save')
def train_model_and_save():
    X, y = get_X_y()
    pipeline = get_ppipeline()
    pipeline.fit(X, y)
    joblib.dump(pipeline, model_path + 'pipeline.pkl')


def get_X_y():
    files_with_dates = []
    last_files = None

    for file_name in os.listdir(csv_path):
        path = csv_path + file_name
        if os.path.isfile(path):
            files_with_dates.append((os.path.getmtime(path), path))

    files_with_dates.sort(key=lambda el: el[0], reverse=True)
    last_files = list(map(lambda x: x[1], files_with_dates[:8]))

    dfs_to_concat = []

    for file in last_files:
        dfs_to_concat.append(pd.read_csv(file, delimiter=';'))

    df = pd.concat(dfs_to_concat)
    df.drop_duplicates('id', inplace=True)

    df = df.rename(columns={'option1': 'condition', 'option2': 'house_type', 'option3': 'balcony', 'option4': 'parking'})

    df = preprocess_data(df)

    df = df.drop(columns=[
        'area_living', 'id', 'author_id', 'address', 'user_address', 'created_at',
        'last_time_up', 'url', 'photo', 'seller', 'price_byn',
        'resale'
    ])

    y = df['price_usd'].to_numpy()
    X = df.drop(columns=['price_usd'])

    return X, y


def preprocess_data(X):
    # X['year'] = X['house_type'].str.extract('(\d+)')
    # X['year'] = X['year'].astype('int')
    # X['year'] = X['year'].fillna(-999)
    X['balcony'] = X['balcony'].str.contains('балконом').astype('int')
    X['house_type'] = X['house_type'].apply(lambda s: s.split(' дом')[0])
    X['parking'] = X['parking'].str.contains('выделенным парковочным местом').astype('int')
    X['area_kitchen'] = X['area_kitchen'].fillna(-999)
    X['first_floor'] = (X['floor'] == 1).astype(int)
    X['last_floor'] = (X['floor'] == X['number_of_floors']).astype(int)
    X['is_new'] = X['condition'].str.contains('Новостройка').astype('int')
    X['renovation'] = X['condition'].str.contains('с ремонтом').astype('int')
    X['house_type'] = X['house_type'].replace({'Панельный': 'panel',
                                               'Блочный': 'block',
                                               'Кирпичный': 'brick',
                                               'Монолитный': 'monolit'}).astype('category')

    X.drop(columns=['condition'], inplace=True)

    X = X[X['area_total'] < 200]
    X = X[X['price_usd'] < 175000]
    X = X[X['price_usd'] > 32000]
    X = X[X['area_kitchen'] < 30]
    X = X[X['number_of_rooms'] < 5]
    #     X = X[X['dist_from_center'] < 0.25]

    return X

def get_ppipeline():
    one_hot_cols = ['house_type', 'number_of_rooms']
    scale_cols = ['latitude',
                  'longitude',
                  'floor',
                  'number_of_floors',
                  'number_of_rooms',
                  'area_total',
                  'area_kitchen']

    col_transformer = make_column_transformer(
        (OneHotEncoder(sparse=False, handle_unknown='ignore'), one_hot_cols),
        (MinMaxScaler(), scale_cols),
        remainder='passthrough', verbose=True)

    lgbm = LGBMRegressor(learning_rate=0.02,
                         num_leaves=41,
                         n_estimators=2000,
                         max_depth=10,
                         colsample_bytree=0.62,
                         reg_lambda=0.81)
    rf = RandomForestRegressor(n_estimators=250, max_features=12, bootstrap=False, n_jobs=-1)

    xgb = XGBRegressor(learning_rate=0.02,
                       num_leaves=41,
                       n_estimators=2000,
                       max_depth=10,
                       colsample_bytree=0.62,
                       reg_lambda=0.81,
                       n_jobs=-1)

    voter = VotingRegressor([
        ('rf', rf),
        ('lgbm', lgbm),
        ('xgb', xgb),
    ], n_jobs=-1)

    pipeline = Pipeline([
        ('custom_transformer', CustomTransformer()),
        ('col_transformer', col_transformer),
        ('estimator', voter)
    ], verbose=True)

    return pipeline

if __name__ == "__main__":
    train_model_and_save()