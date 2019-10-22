from flask import Blueprint, render_template, request, jsonify, abort
import joblib
import os
import sqlite3
from pathlib import Path
from helpers import dist_center, dist_metro, get_data_object_from_request

model_path = str(Path(__file__).parent.absolute()) + '/../ml_models/'
db_path = str(Path(__file__).parent.absolute()) + '/../db/'

is_docker = os.environ.get('IS_DOCKER', False)
if is_docker:
    model_path = '/mounted/models/'
    db_path = '/mounted/db/'

predict = Blueprint('predict', __name__)
model = joblib.load(model_path + 'pipeline.pkl')

@predict.route('/predict', methods=['POST'])
def predict_price():

    if request.headers.get('Host') not in ['0.0.0.0:5000', '0.0.0.0:5001', 'realtorbot.by']:
        return abort(401)

    global model
    if not model:
        model = joblib.load(model_path + 'pipeline.pkl')

    X = get_data_object_from_request(request)
    area_total = X['area_total'].values[0]
    price = model.predict(X)[0] * 0.96  # обычно, 4% в среднем скидывает продавец


    return jsonify({
        'price': price,
        'square_price': price / area_total
    })


@predict.route('/api/get_apartment_price', methods=['POST'])
def api_get_apartment_price():
    try:
        key = request.form.get('key')
        if not key:
            return abort(401)

        conn = sqlite3.connect(db_path + 'realtorbot.db')
        cursor = conn.execute('SELECT * FROM api_users WHERE key=?', (key,))

        api_user = cursor.fetchone()

        if not api_user:
            return abort(401)

    # return '1'

        X = get_data_object_from_request(request)
        area_total = X['area_total'].values[0]
        global model
        if not model:
            model = joblib.load(model_path + 'pipeline.pkl')



        price = model.predict(X)[0] * 0.96  # обычно, 4% в среднем скидывает продавец

        if price:
            conn.execute('UPDATE api_users SET request_counter = cast(request_counter as INTEGER) + 1 WHERE key=?', (key,))
            conn.commit()
            conn.close()
    except:
        return abort(500)

    return jsonify({
        'price': price,
        'm2_price': price / area_total
    })