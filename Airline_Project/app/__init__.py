from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)

    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Airline Ticketing API",
            "description": "Flight and Ticket Management System",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    })

    from app.routes.auth_routes import auth_bp
    from app.routes.flight_routes import flight_bp
    from app.routes.ticket_routes import ticket_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(flight_bp, url_prefix='/api/v1/flight')
    app.register_blueprint(ticket_bp, url_prefix='/api/v1/ticket')

    return app
