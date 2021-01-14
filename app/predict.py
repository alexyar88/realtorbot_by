from flask import Blueprint, render_template, request, jsonify, abort
import pickle
import os
import sqlite3
import utils

predict = Blueprint('predict', __name__)

model_dir = '../../mounted/model'
pipeline_path = os.path.join(model_dir, 'pipeline.pkl')
# with open(pipeline_path, 'rb') as file:
#     pipeline = pickle.load(file)

@predict.route('/predict', methods=['POST'])
def predict_price():
    #
    # referer = request.headers.get('Referer')
    # is_parser = True
    #
    # for domain in ['0.0.0.0:5000', '0.0.0.0:5001', 'realtorbot.by']:
    #     if referer and domain in referer:
    #         is_parser = False
    #         break
    #
    #
    # if is_parser:
    #     return abort(401)

    # global pipeline
    # if pipeline is None:
    with open(pipeline_path, 'rb') as pipeline_file:
        pipeline = pickle.load(pipeline_file)

    X = utils.get_data_object_from_request(request)
    area_total = X['area_total'].values[0]

    correction = 0.96  # common sale discount is 4%
    price = pipeline.predict(X)[0]
    price_lower, price_upper = pipeline.predict(X, return_dist=True)[0].dist.interval(0.80)



    return jsonify({
        'price': price * correction,
        'square_price': price / area_total * correction,
        'price_upper': price_upper * correction,
        'price_lower': price_lower * correction,
    })


# @predict.route('/api/get_apartment_price', methods=['POST'])
# def api_get_apartment_price():
#     try:
#         key = request.form.get('key')
#         if not key:
#             return abort(401)
#
#         conn = sqlite3.connect(db_path + 'realtorbot.db')
#         cursor = conn.execute('SELECT * FROM api_users WHERE key=?', (key,))
#
#         api_user = cursor.fetchone()
#
#         if not api_user:
#             return abort(401)
#
#     # return '1'
#
#         X = get_data_object_from_request(request)
#         area_total = X['area_total'].values[0]
#         global model
#         if not model:
#             model = joblib.load(model_path + 'pipeline.pkl')
#
#
#
#         price = model.predict(X)[0] * 0.96  # обычно, 4% в среднем скидывает продавец
#
#         if price:
#             conn.execute('UPDATE api_users SET request_counter = cast(request_counter as INTEGER) + 1 WHERE key=?', (key,))
#             conn.commit()
#             conn.close()
#     except:
#         return abort(500)
#
#     return jsonify({
#         'price': price,
#         'm2_price': price / area_total
#     })