from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.ticket_service import buy_ticket, checkin_passenger, get_passenger_list

ticket_bp = Blueprint("ticket_bp", __name__)

@ticket_bp.route('/', methods=['POST'])
@jwt_required()
def purchase_ticket():
    """
    Buy a ticket
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            flight_id:
              type: integer
            passenger_name:
              type: string
    responses:
      200:
        description: Ticket purchased
    """
    data = request.get_json()
    return buy_ticket(data.get("flight_id"), data.get("passenger_name"))

@ticket_bp.route('/checkin', methods=['POST'])
def checkin():
    """
    Check in to assign a seat
    ---
    tags:
      - Tickets
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            flight_id:
              type: integer
            passenger_name:
              type: string
    responses:
      200:
        description: Seat assigned
    """
    data = request.get_json()
    return checkin_passenger(data.get("flight_id"), data.get("passenger_name"))

@ticket_bp.route('/<int:flight_id>/passengers', methods=['GET'])
@jwt_required()
def passengers(flight_id):
    """
    Get Passenger List for a Flight
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - name: flight_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: List of passengers
    """
    return get_passenger_list(flight_id)
