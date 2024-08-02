from flask import Flask

def create_app():
    app = Flask(__name__)

    from .blueprints.check_availability_blueprint import check_availability_bp
    #from .blueprints.place_order_blueprint import place_order_bp
    app.register_blueprint(check_availability_bp, url_prefix='/check_availability')
    #app.register_blueprint(place_order_bp, url_prefix='/place_order')

    return app