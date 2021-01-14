from ngboost import NGBRegressor
from ngboost.distns import Normal, LogNormal, Poisson, Exponential

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeRegressor
from sklearn.cluster import KMeans

import numpy as np


class FeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.km = KMeans(n_clusters=64)
        self.km.fit(X[['latitude', 'longitude']])
        return self

    def transform(self, X, y=None):
        X = X.copy()

        # removing \xa0 symbol
        X['balcony'] = X['balcony'].str.replace('\\xa0', ' ', regex=True)
        X['condition'] = X['condition'].str.replace('\\xa0', ' ', regex=True)
        X['house_type'] = X['house_type'].str.replace('\\xa0', ' ', regex=True)
        X['parking'] = X['parking'].str.replace('\\xa0', ' ', regex=True)

        # making clusters for geo
        X['geocluster'] = self.km.predict(X[['latitude', 'longitude']])

        # rotating coordinated
        X['latitude30'], X['longitude30'] = self.rotate_latlng(X['latitude'], X['longitude'], 30)
        X['latitude45'], X['longitude45'] = self.rotate_latlng(X['latitude'], X['longitude'], 45)
        X['latitude60'], X['longitude60'] = self.rotate_latlng(X['latitude'], X['longitude'], 60)

        X['year'] = X['house_type'].str.extract('(\d+)').astype(float)
        X['house_material'] = X['house_type'].str.split(' дом').str[0]

        X = X.drop(columns=['house_type'])

        return X

    @staticmethod
    def rotate_latlng(lat, lng, degrees):
        rads = degrees / 180 * np.pi
        lat_new = lat * np.cos(rads) + lng * np.sin(rads)
        lng_new = lng * np.cos(rads) - lat * np.sin(rads)

        return lat_new, lng_new


class NGBRegressorCustom(BaseEstimator):
    def __init__(self, **kwargs):
        self.estimator = NGBRegressor(**kwargs)

    def fit(self, X, y=None, **kwargs):
        self.estimator.fit(X, y, **kwargs)
        return self

    def predict(self, X, return_dist=False, **kwargs):
        if return_dist:
            return self.estimator.pred_dist(X, **kwargs)
        else:
            return self.estimator.predict(X, **kwargs)


def build():
    column_transformer = make_column_transformer(
        (SimpleImputer(strategy='constant', fill_value=-1), ['area_kitchen', 'year']),
        (OneHotEncoder(drop='if_binary'), ['resale', 'condition', 'house_material', 'balcony', 'parking']),
        remainder='passthrough',
        sparse_threshold=0
    )

    pipeline = Pipeline([
        ('feature_extractor', FeatureExtractor()),
        ('column_transformer', column_transformer),
        ('estimator', NGBRegressorCustom(
            n_estimators=2000,
            learning_rate=0.05,
            Dist=LogNormal,
            Base=DecisionTreeRegressor(
                max_depth=7,
                criterion='friedman_mse'
            )
        ))
    ])

    return pipeline
