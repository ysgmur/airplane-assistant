from flask import jsonify
from app import db
from app.models.flight_model import Flight
from app.models.ticket_model import Ticket
from app.schemas.flight_schema import flight_schema, flights_schema
from sqlalchemy import func, or_

def create_flight(data):
    flight = flight_schema.load(data)
    db.session.add(flight)
    db.session.commit()
    return jsonify(flight_schema.dump(flight)), 201

def get_available_flights(page, page_size):
    subquery = db.session.query(
        Ticket.flight_id,
        func.count(Ticket.id).label('ticket_count')
    ).group_by(Ticket.flight_id).subquery()

    flights = db.session.query(Flight).outerjoin(
        subquery, Flight.id == subquery.c.flight_id
    ).filter(
        or_(
            subquery.c.ticket_count == None,
            subquery.c.ticket_count < Flight.capacity
        )
    ).paginate(page=page, per_page=page_size, error_out=False)

    return jsonify({
        "page": page,
        "page_size": page_size,
        "total": flights.total,
        "flights": flights_schema.dump(flights.items)
    })
