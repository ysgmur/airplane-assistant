from flask import current_app
from app.models.flight_model import Flight
from app.models.ticket_model import Ticket
from app import db

def call_airline_api(parsed, passenger_name):
    intent = parsed.get("intent")
    passenger_name = passenger_name.strip().lower()

    with current_app.app_context():

        if intent == "buy":
            flight = Flight.query.filter_by(
                airport_from=parsed.get("from"),
                airport_to=parsed.get("to"),
                date_from=parsed.get("date")
            ).first()

            if not flight:
                return {"msg": "No matching flights found"}

            ticket_count = Ticket.query.filter_by(flight_id=flight.id).count()
            if ticket_count >= flight.capacity:
                return {"msg": "No seats available"}

            # Zaten almış mı?
            existing = Ticket.query.filter_by(
                flight_id=flight.id,
                passenger_name=passenger_name
            ).first()
            if existing:
                return {
                    "msg": "You already booked this flight",
                    "ticket_id": existing.id,
                    "seat": existing.seat_number
                }

            ticket = Ticket(
                flight_id=flight.id,
                passenger_name=passenger_name
            )
            db.session.add(ticket)
            db.session.commit()

            return {
                "msg": "Ticket booked",
                "ticket_id": ticket.id,
                "passenger_name": passenger_name
            }

        elif intent == "checkin":
            ticket = None

            if "ticket_id" in parsed:
                ticket = Ticket.query.get(parsed["ticket_id"])

            elif "flight_id" in parsed:
                ticket = Ticket.query.filter_by(
                    flight_id=parsed["flight_id"],
                    passenger_name=passenger_name
                ).first()

            elif all(k in parsed for k in ["from", "to", "date"]):
                flight = Flight.query.filter_by(
                    airport_from=parsed["from"],
                    airport_to=parsed["to"],
                    date_from=parsed["date"]
                ).first()
                if flight:
                    ticket = Ticket.query.filter_by(
                        flight_id=flight.id,
                        passenger_name=passenger_name
                    ).first()

            if not ticket:
                return {"error": "Ticket not found"}

            if ticket.seat_number:
                return {
                    "message": "Already checked in",
                    "seat_number": ticket.seat_number,
                    "ticket_id": ticket.id
                }

            existing_seats = [t.seat_number for t in Ticket.query.filter(
                Ticket.flight_id == ticket.flight_id,
                Ticket.seat_number != None
            ).all()]

            seat_number = str(len(existing_seats) + 1)
            ticket.seat_number = seat_number
            db.session.commit()

            return {
                "message": "Check-in successful",
                "seat_number": seat_number,
                "ticket_id": ticket.id
            }

        elif intent == "search":
            flights = Flight.query.filter_by(
                airport_to=parsed.get("to"),
                date_from=parsed.get("date")
            ).all()
            return {
                "results": [f"{f.airport_from} → {f.airport_to} on {f.date_from}" for f in flights]
            }

        elif intent == "add_flight":
            flight = Flight(
                airport_from=parsed.get("from"),
                airport_to=parsed.get("to"),
                date_from=parsed.get("date"),
                date_to=parsed.get("date"),
                capacity=parsed.get("capacity", 100),
                duration=parsed.get("duration", 120)
            )
            db.session.add(flight)
            db.session.commit()
            return {
                "message": "Flight created",
                "flight_id": flight.id
            }

        else:
            return {"msg": "Intent not recognized"}
