from flask import Flask
from pages import pages
import parser
import trainer
from predict import predict

tempalte_dir = '../templates'
static_dir = '../static'

app = Flask(__name__, template_folder=tempalte_dir, static_folder=static_dir)
app.register_blueprint(pages)
app.register_blueprint(predict)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # parser.schedule_parser('/some/path')
