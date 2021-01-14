import time
import csv
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

columns = ('id', 'author_id', 'address', 'user_address', 'latitude', 'longitude', 'resale', 'floor',
           'number_of_floors', 'number_of_rooms', 'area_total', 'area_living', 'area_kitchen', 'seller',
           'created_at', 'last_time_up', 'url', 'photo', 'condition', 'house_type', 'balcony', 'parking',
           'price_byn', 'price_usd')


def parse_data_to_csv(csv_dir, column_names=columns):
    time_string = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    result_csv_path = os.path.join(csv_dir, f'onliner_minsk_{time_string}.csv')
    with open(result_csv_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(column_names)

        for area in range(1, 500):
            page_num = 1

            while True:
                search_page_url = get_search_results_page_url(area, area + 1, page_num)
                search_page_json = requests.get(search_page_url).json()
                last_page_num = search_page_json['page']['last']

                search_page_results_json = search_page_json['apartments']
                write_search_page_results_to_csv(search_page_results_json, writer)
                page_num += 1

                if page_num > last_page_num:
                    break


def write_search_page_results_to_csv(search_page_results_json, writer):
    time.sleep(0.06)
    for apartment in search_page_results_json:
        apartment.setdefault('')
        apartment_page = requests.get(apartment.get('url'))
        parser = BeautifulSoup(apartment_page.content, 'html.parser')
        apartment_options = parser.select('ul.apartment-options li.apartment-options__item')
        options = [option.get_text(strip=True) for option in apartment_options]

        # page data must have at least 4 options
        if len(options) < 4:
            continue

        apartment_arr = [
            apartment.get('id'),
            apartment.get('author_id'),
            apartment.get('location', dict()).get('address', ''),
            apartment.get('location', dict()).get('user_address', ''),
            apartment.get('location', dict()).get('latitude', ''),
            apartment.get('location', dict()).get('longitude', ''),
            apartment.get('resale'),
            apartment.get('floor'),
            apartment.get('number_of_floors'),
            apartment.get('number_of_rooms'),
            apartment.get('area', dict()).get('total', ''),
            apartment.get('area', dict()).get('living', ''),
            apartment.get('area', dict()).get('kitchen', ''),
            apartment.get('seller', dict()).get('type', ''),
            apartment.get('created_at'),
            apartment.get('last_time_up'),
            apartment.get('url'),
            apartment.get('photo'),
            options[0],
            options[1],
            options[2],
            options[3],
            apartment.get('price', dict()).get('converted', dict()).get('BYN', dict()).get('amount', 0),
            apartment.get('price', dict()).get('converted', dict()).get('USD', dict()).get('amount', 0),
        ]
        writer.writerow(apartment_arr)


def get_search_results_page_url(area1, area2, n):
    return f"https://pk.api.onliner.by/search/apartments?" \
           f"area%5Bmin%5D={area1}&area%5Bmax%5D={area2}&" \
           f"bounds%5Blb%5D%5Blat%5D=53.820922446131" \
           f"&bounds%5Blb%5D%5Blong%5D=27.344970703125" \
           f"&bounds%5Brt%5D%5Blat%5D=53.97547425743" \
           f"&bounds%5Brt%5D%5Blong%5D=27.77961730957" \
           f"&v=0.12052430637493972" \
           f"&page={n}"


if __name__ == '__main__':
    parse_data_to_csv('../../mounted/data')
