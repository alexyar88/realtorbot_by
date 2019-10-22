import numpy as np
import pandas as pd


def count_dist(lat1, long1, lat2, long2):
    return np.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)

def dist_center(lat, long):
    city_center = [53.904541, 27.561523]
    return count_dist(city_center[0], city_center[1], lat, long)

def dist_metro(lat, long):
    metro_stations = [
        [53.9456795, 27.6901145],
        [53.9384013, 27.6649479],
        [53.9342655, 27.6511542],
        [53.9270232, 27.6266416],
        [53.92470492, 27.6145649],
        [53.9211386, 27.5977205],
        [53.91548013, 27.58291483],
        [53.9081672, 27.5742143],
        [53.90210688, 27.56172538],
        [53.8936421, 27.54785299],
        [53.8860921, 27.5374843],
        [53.88660473, 27.51588643],
        [53.87677066, 27.4973309],
        [53.86430874, 27.48530388],
        [53.8483949, 27.4737483],
        [53.86146792, 27.67532229],
        [53.86898398, 27.64744878],
        [53.87519573, 27.6286304],
        [53.8891415, 27.6155278],
        [53.88997814, 27.5863266],
        [53.89361681, 27.5701797],
        [53.9001631, 27.56267488],
        [53.90558332, 27.55456924],
        [53.90524833, 27.53919482],
        [53.906642, 27.52291381],
        [53.90929648, 27.49634922],
        [53.90834531, 27.48084605],
        [53.90602576, 27.45420098],
        [53.90673997, 27.43609071]
    ]

    distances = []

    for station in metro_stations:
        distances.append(count_dist(lat, long, station[0], station[1]))
    return min(distances)

def get_data_object_from_request(request):
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

    return X