from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "https://tileselection.com.au"}})
    
    from .blueprints.check_availability_blueprint import check_availability_bp
    #from .blueprints.place_order_blueprint import place_order_bp
    app.register_blueprint(check_availability_bp, url_prefix='/check_availability')
    #app.register_blueprint(place_order_bp, url_prefix='/place_order')

    return app
