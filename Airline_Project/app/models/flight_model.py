from app import db

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.String(50))
    date_to = db.Column(db.String(50))
    airport_from = db.Column(db.String(100))
    airport_to = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    capacity = db.Column(db.Integer)

    tickets = db.relationship("Ticket", backref="flight", lazy=True)
