from app.models.flight_model import Flight
from app import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class FlightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        sqla_session = db.session

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)
