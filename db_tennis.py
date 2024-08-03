from db import db
from datetime import datetime

class Tennis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    player = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float)
    location = db.Column(db.String(200))
    category = db.Column(db.String(200))
    details = db.Column(db.String(200))
    reflection = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Tennis %r>' % self.id

class TennisAnalysis:
    pass  # Empty class definition

class TennisStatus:
    pass  # Empty class definition

def save_reflection(tennis_id, reflect):
    tennis = Tennis.query.get_or_404(tennis_id)
    tennis.reflection = reflect
    db.session.commit()