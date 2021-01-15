from flask import Blueprint, request, jsonify
import pickle
import os
import utils

predict = Blueprint('predict', __name__)

model_dir = '../../mounted/model'
pipeline_path = os.path.join(model_dir, 'pipeline.pkl')

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

    correction = 0.87  # mean sale discount is 13% because of crisis
    price = pipeline.predict(X)[0]
    price_lower, price_upper = pipeline.predict(X, return_dist=True)[0].dist.interval(0.80)



    return jsonify({
        'price': price * correction,
        'square_price': price / area_total * correction,
        'price_upper': price_upper * correction,
        'price_lower': price_lower * correction,
    })
