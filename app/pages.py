from flask import Blueprint, render_template, request

pages = Blueprint('pages', __name__)

@pages.route('/')
def index_page():
    return render_template('index.html', img='start-minsk-1.jpg')

@pages.route('/price')
def price_page():
    lat = request.args.get('lat')
    long = request.args.get('long')
    address = request.args.get('address')
    return render_template('check-the-price.html', lat=lat, long=long, address=address)

@pages.route('/about')
def about_page():
    return render_template('about.html')

@pages.route('/api')
def api_page():
    return render_template('get-api.html')

