from flask import Flask
from pages import pages
from parser import parser
from train_model import train_model
from predict import predict



tempalte_dir = '../templates'
static_dir = '../static'



app = Flask(__name__, template_folder=tempalte_dir, static_folder=static_dir)
app.register_blueprint(pages)
app.register_blueprint(parser)
app.register_blueprint(train_model)
app.register_blueprint(predict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')