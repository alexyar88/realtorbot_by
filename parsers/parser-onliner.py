import requests
import time
import math
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime


def get_page(area1, area2, n):
    return "https://pk.api.onliner.by/search/apartments?area%5Bmin%5D={}&area%5Bmax%5D={}&bounds%5Blb%5D%5Blat%5D=50.91688748924508&bounds%5Blb%5D%5Blong%5D=20.566406250000004&bounds%5Brt%5D%5Blat%5D=56.607885465009254&bounds%5Brt%5D%5Blong%5D=34.62890625000001&page={}".format(
        area1, area2, n)

def get_page_minsk(area1, area2, n):
    return "https://pk.api.onliner.by/search/apartments?area%5Bmin%5D={}&area%5Bmax%5D={}&bounds%5Blb%5D%5Blat%5D=53.820922446131&bounds%5Blb%5D%5Blong%5D=27.344970703125&bounds%5Brt%5D%5Blat%5D=53.97547425743&bounds%5Brt%5D%5Blong%5D=27.77961730957&v=0.12052430637493972&page={}".format(
        area1, area2, n)


def parse_flats(flats, writer):
    time.sleep(0.06)
    for flat in flats:
        flat.setdefault('')
        page = requests.get(flat.get('url'))
        parser = BeautifulSoup(page.content, 'html.parser')
        flat_options = parser.select('ul.apartment-options li.apartment-options__item')
        options = [option.text for option in flat_options]
        if len(options) < 4:
            print('Skipped: ', flat.get('url'))
            continue
        flat_arr = [
            flat.get('id'),
            flat.get('author_id'),
            flat.get('location', dict()).get('address', ''),
            flat.get('location', dict()).get('user_address', ''),
            flat.get('location', dict()).get('latitude', ''),
            flat.get('location', dict()).get('longitude', ''),
            flat.get('resale'),
            flat.get('floor'),
            flat.get('number_of_floors'),
            flat.get('number_of_rooms'),
            flat.get('area', dict()).get('total', ''),
            flat.get('area', dict()).get('living', ''),
            flat.get('area', dict()).get('kitchen', ''),
            flat.get('seller', dict()).get('type', ''),
            flat.get('created_at'),
            flat.get('last_time_up'),
            flat.get('url'),
            flat.get('photo'),
            options[0],
            options[1],
            options[2],
            options[3],
            flat.get('price', dict()).get('converted', dict()).get('BYN', dict()).get('amount', 0),
            flat.get('price', dict()).get('converted', dict()).get('USD', dict()).get('amount', 0),
        ]
        writer.writerow(flat_arr)


# result_json = requests.get(get_page()).json()
# flats = result_json['apartments']
# total = result_json['total']
# pages = math.ceil(total / 96)
time_string = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

columns = ['id', 'author_id', 'address', 'user_address', 'latitude', 'longitude', 'resale', 'floor', 'number_of_floors', 'number_of_rooms', 'area_total', 'area_living', 'area_kitchen', 'seller', 'created_at', 'last_time_up', 'url',
           'photo', 'option1', 'option2', 'option3', 'option4','price_byn', 'price_usd']

with open('./data/flats_minsk_{}.csv'.format(time_string), 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(columns)

    for area in range(1, 1001):
        # result_json = requests.get(get_page(area, area + 1, 1)).json()
        # flats = result_json['apartments']
        # total = result_json['total']
        # pages = math.ceil(total / 96)

        page_num = 1
        page_last = 10000

        while True:
            page_result_json = requests.get(get_page_minsk(area, area + 1, page_num)).json()
            page_last = page_result_json['page']['last']

            print('Page:', page_num, ', Area: ', area)
            print(page_result_json['page'])

            flats = page_result_json['apartments']
            parse_flats(flats, writer)
            page_num += 1

            if page_num > page_last:
                break

print('Done!')
