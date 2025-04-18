from flask import Flask, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from config import DevelopmentConfig
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
jwt = JWTManager()

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Entrer le token sous la forme: Bearer <votre_token>"
    }
}

db = SQLAlchemy()

def create_app(config_class='config.DevelopmentConfig'):
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admins import api as admin_ns

    app = Flask(__name__)
    CORS(app, origins=["http://localhost:8000"], supports_credentials=True)



    app.config.from_object(config_class)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        security="Bearer Auth",
        authorizations=authorizations
        )
    # Register the admin namespace
    api.add_namespace(admin_ns, path='/api/v1/admin')
    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # Register the auth namespace
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    return app
