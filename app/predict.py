from flask import Blueprint, render_template, request, jsonify
import joblib
import pandas as pd
import os
from pathlib import Path
from helpers import dist_center, dist_metro

model_path = str(Path(__file__).parent.absolute()) + '/../ml_models/'

is_docker = os.environ.get('IS_DOCKER', False)
if is_docker:
    model_path = '/mounted/models/'

predict = Blueprint('predict', __name__)


@predict.route('/predict', methods=['POST'])
def predict_price():

    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    floor = int(request.form.get('floor'))
    number_of_floors = int(request.form.get('number-of-floors'))
    rooms = int(request.form.get('rooms'))
    area_total = float(request.form.get('area-total'))
    area_kitchen = float(request.form.get('area-kitchen') if request.form.get('area-kitchen') else -999)
    house_type = request.form.get('house-type')
    balcony = int(1 if request.form.get('balcony') else 0)
    parking = int(1 if request.form.get('parking') else 0)
    year = int(request.form.get('year') if request.form.get('year') else -999)
    first_floor = int(floor == 1)
    last_floor = int(floor == number_of_floors)
    is_new = int(request.form.get('is-new'))
    is_renovated = int(1 if request.form.get('is-renovated') else 0)

    X_arr = [
        latitude,
        longitude,
        floor,
        number_of_floors,
        rooms,
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

    print(X_arr)

    columns = ['latitude', 'longitude', 'floor', 'number_of_floors', 'number_of_rooms',
       'area_total', 'area_kitchen', 'house_type', 'balcony', 'parking', 'year', 'first_floor', 'last_floor',
       'is_new', 'renovation']



    X = pd.DataFrame([X_arr], columns=columns)
    model = joblib.load(model_path + 'pipeline.pkl')
    price = model.predict(X)[0] * 0.96  # обычно, 4% в среднем скидывает продавец


    return jsonify({
        'price': price,
        'square_price': price / area_total
    })

