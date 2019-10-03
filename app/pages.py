from flask import Blueprint, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import time
import os
from pathlib import Path
from helpers import dist_center, dist_metro




model_path = str(Path(__file__).parent.absolute()) + '/../ml_models/'

is_docker = os.environ.get('IS_DOCKER', False)
if is_docker:
    model_path = '/mounted/models/'


pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return render_template('index.html')


@pages.route('/predict', methods=['POST'])
def predict():

    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    floor = int(request.form['floor'])
    number_of_floors = int(request.form['number-of-floors'])
    rooms = int(request.form['rooms'])
    area_total = float(request.form['area-total'])
    area_kitchen = float(request.form['area-kitchen'])
    house_type = request.form['house-type']
    balcony = int(request.form['balcony'])
    parking = int(request.form['parking'])
    year = int(request.form['year'])
    first_floor = int(floor == 1)
    last_floor = int(floor == number_of_floors)
    is_new = int(request.form['is-new'])
    is_renovated = int(request.form['is-renovated'])

    # dist_from_center = dist_center(latitude, longitude)
    # dist_from_metro = dist_metro(latitude, longitude)
    #
    # house_type_ohe = [0] * 4
    # house_type_ohe[house_type] = 1
    # flat_type_ohe = [0] * 4


    X_arr = [
        latitude,
        longitude,
        floor,
        number_of_floors,
        rooms + 1,
        area_total,
        area_kitchen,
        house_type,
        balcony,
        parking,
        year,
        first_floor,
        last_floor,
        is_new,
        is_renovated
    ]

    columns = ['latitude', 'longitude', 'floor', 'number_of_floors', 'number_of_rooms',
       'area_total', 'area_kitchen', 'house_type', 'balcony', 'parking', 'year', 'first_floor', 'last_floor',
       'is_new', 'renovation']



    X = pd.DataFrame([X_arr], columns=columns)
    model = joblib.load(model_path + 'pipeline.pkl')
    price = model.predict(X)[0] * 0.97  # обычно, 3% в среднем скидывает продавец


    time.sleep(0.3)


    return jsonify({
        'price': price,
        'square_price': price / area_total
    })

