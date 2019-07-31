from flask import Flask, render_template, request, url_for
import os
import joblib
import numpy as np
import pandas as pd
import time
import json
from dist_helpers import dist_center, dist_metro

tempalte_dir = os.path.abspath('../templates/')
static_dir = os.path.abspath('../static/')

app = Flask(__name__, template_folder=tempalte_dir, static_folder=static_dir)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    print(request.form['latitude'])

    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    floor = int(request.form['floor'])
    number_of_floors = int(request.form['number-of-floors'])
    rooms = int(request.form['rooms'])
    area_total = float(request.form['area-total'])
    area_kitchen = float(request.form['area-kitchen'])
    balcony = int(request.form['balcony'])
    parking = int(request.form['parking'])
    year = int(request.form['year'])
    house_type = int(request.form['house-type'])
    is_new = int(request.form['is-new'])
    is_renovated = int(request.form['is-renovated'])

    dist_from_center = dist_center(latitude, longitude)
    dist_from_metro = dist_metro(latitude, longitude)
    first_floor = int(floor == 1)
    last_floor = int(floor == number_of_floors)
    # rooms_ohe = [0] * 4
    # rooms_ohe[rooms] = 1
    house_type_ohe = [0] * 4
    house_type_ohe[house_type] = 1
    flat_type_ohe = [0] * 4

    # print(house_type_ohe)

    if is_new:
        if is_renovated:
            flat_type_ohe[3] = 1
        else:
            flat_type_ohe[2] = 1
    else:
        if is_renovated:
            flat_type_ohe[1] = 1
        else:
            flat_type_ohe[0] = 1

    print(flat_type_ohe)

    X_arr = [
        latitude,
        longitude,
        floor,
        number_of_floors,
        rooms + 1,
        area_total,
        area_kitchen,
        balcony,
        parking,
        dist_from_center,
        dist_from_metro,
        year,
        first_floor,
        last_floor,
        # *rooms_ohe,
        *flat_type_ohe,
        *house_type_ohe,

    ]

    print(X_arr)

    X = np.array([X_arr])

    # X_my = np.array([[53.8461849, 27.469189099999994, 1, 7, 9, 53, 9, 1, 0, 0.10922904145153806, np.log(0.005066596948651071), 2000, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]])
    columns = ['latitude', 'longitude', 'floor', 'number_of_floors', 'number_of_rooms',
       'area_total', 'area_kitchen', 'balcony', 'parking', 'dist_from_center',
       'dist_from_metro', 'year', 'first_floor', 'last_floor',
       'Вторичка без отделки', 'Вторичка с ремонтом',
       'Новостройка без отделки', 'Новостройка с ремонтом', 'Блочный',
       'Кирпичный', 'Монолитный', 'Панельный']




    X = pd.DataFrame(X, columns=columns)

    scaler = joblib.load('../ml_models/scaler_model.pkl')
    columns_to_scale = ['latitude', 'longitude', 'dist_from_metro', 'dist_from_center']
    X[columns_to_scale] = scaler.transform(X[columns_to_scale])

    model = joblib.load('../ml_models/voter_model.pkl')
    price = model.predict(X)[0]


    time.sleep(0.3)


    # return json.dump({
    #     'price': price,
    #     'square_price': price / area_total
    # })
    return str(price)

if __name__ == "__main__":
    app.run(debug=True)
