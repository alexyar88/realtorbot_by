import pandas as pd


def get_data_object_from_request(request):
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    resale = bool(1 - int(request.form.get('is-new')))
    floor = int(request.form.get('floor'))
    number_of_floors = int(request.form.get('number-of-floors'))
    rooms = int(request.form.get('rooms'))
    area_total = float(request.form.get('area-total'))
    area_kitchen = float(request.form.get('area-kitchen') if request.form.get('area-kitchen') else None)
    house_material = request.form.get('house-type')
    year = int(request.form.get('year') if request.form.get('year') else None)
    is_renovated = int(1 if request.form.get('is-renovated') else 0)
    condition = get_condition(resale=resale, is_renovated=is_renovated)
    house_type = get_house_type(house_material=house_material, year=year)
    balcony = 'С балконом (лоджией)' if request.form.get('balcony') else 'Без балкона (лоджии)'
    parking = 'С выделенным парковочным местом на улице' if request.form.get(
        'parking') else 'Без выделенного парковочного места'

    X_arr = [
        latitude,
        longitude,
        resale,
        floor,
        number_of_floors,
        rooms,
        area_total,
        area_kitchen,
        condition,
        house_type,
        balcony,
        parking,
    ]



    columns = [
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
    ]

    X = pd.DataFrame([X_arr], columns=columns)
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(X)
    return X


def get_condition(resale, is_renovated):
    if resale and is_renovated:
        return 'Вторичка с ремонтом'
    if resale and not is_renovated:
        return 'Вторичка без отделки'
    if not resale and is_renovated:
        return 'Новостройка с ремонтом'
    if not resale and not is_renovated:
        return 'Новостройка без отделки'


def get_house_type(house_material, year):
    if year is None:
        return f'{house_material} дом'
    else:
        return f'{house_material} дом {year} года'
