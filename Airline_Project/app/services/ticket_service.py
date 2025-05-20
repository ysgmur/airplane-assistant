from flask import jsonify
from app import db
from app.models.ticket_model import Ticket
from app.models.flight_model import Flight

def buy_ticket(flight_id, passenger_name):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"error": "Flight not found"}), 404

    ticket_count = Ticket.query.filter_by(flight_id=flight_id).count()
    if ticket_count >= flight.capacity:
        return jsonify({"error": "No seats available"}), 400

    ticket = Ticket(flight_id=flight_id, passenger_name=passenger_name)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "id": ticket.id,
        "passenger_name": ticket.passenger_name
    })


def checkin_passenger(flight_id, passenger_name):
    ticket = Ticket.query.filter_by(flight_id=flight_id, passenger_name=passenger_name).first()
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    if ticket.seat_number:
        return jsonify({
            "message": "Already checked in",
            "seat_number": ticket.seat_number
        })

    existing_seats = [t.seat_number for t in Ticket.query.filter(
        Ticket.flight_id == flight_id,
        Ticket.seat_number != None
    ).all()]

    seat_number = str(len(existing_seats) + 1)
    ticket.seat_number = seat_number
    db.session.commit()

    return jsonify({"seat_number": seat_number})


def get_passenger_list(flight_id):
    tickets = Ticket.query.filter_by(flight_id=flight_id).all()
    return jsonify([{
        "passenger_name": t.passenger_name,
        "seat_number": t.seat_number
    } for t in tickets])
