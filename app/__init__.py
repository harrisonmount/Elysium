from flask import Flask, send_from_directory
from .database import db
from app.routes.api_handlers import api_blueprint

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(api_blueprint)

    @app.route('/')
    def home():
        return send_from_directory(app.static_folder, 'index.html')

    db.init_app(app)

    with app.app_context():
        db.create_all()
    return app
