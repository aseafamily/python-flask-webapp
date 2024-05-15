from db import db
from datetime import datetime

class Serve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    player = db.Column(db.Integer, nullable=False)
    first_serve_in = db.Column(db.Integer, default=0)
    first_serve_out = db.Column(db.Integer, default=0)
    second_serve_in = db.Column(db.Integer, default=0)
    second_serve_out = db.Column(db.Integer, default=0)
    total_first_serve = db.Column(db.Integer, default=0)
    total_second_serve = db.Column(db.Integer, default=0)
    first_serve_in_percent = db.Column(db.Integer, default=0)
    second_serve_in_percent = db.Column(db.Integer, default=0)
    total_serve = db.Column(db.Integer, default=0)
    total_serve_in = db.Column(db.Integer, default=0)
    total_serve_out = db.Column(db.Integer, default=0)
    total_serve_percent = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
    location = db.Column(db.String(200))
    comment = db.Column(db.String(1000))
    first_serve_in_deuce = db.Column(db.Integer, default=0)
    first_serve_out_deuce = db.Column(db.Integer, default=0)
    second_serve_in_deuce = db.Column(db.Integer, default=0)
    second_serve_out_deuce = db.Column(db.Integer, default=0)
    first_serve_in_percent_deuce = db.Column(db.Integer, default=0)
    second_serve_in_percent_deuce = db.Column(db.Integer, default=0)
    first_serve_in_ad = db.Column(db.Integer, default=0)
    first_serve_out_ad = db.Column(db.Integer, default=0)
    second_serve_in_ad = db.Column(db.Integer, default=0)
    second_serve_out_ad = db.Column(db.Integer, default=0)
    first_serve_in_percent_ad = db.Column(db.Integer, default=0)
    second_serve_in_percent_ad = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Serve %r>' % self.id
    
class ServeAnalysis:
    pass  # Empty class definition

class ServeStatus:
    pass  # Empty class definition