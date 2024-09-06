from db import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'player'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.CHAR(1), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    year_graduation = db.Column(db.Integer, nullable=True)
    utr_profile = db.Column(db.String(200), nullable=True)
    usta_profile = db.Column(db.String(200), nullable=True)
    usta_id = db.Column(db.Integer, nullable=True)
    utr = db.Column(db.Integer, nullable=True)
    wtn = db.Column(db.Integer, nullable=True)
    usta = db.Column(db.Integer, nullable=True)
    utr_date = db.Column(db.Date, nullable=True)
    wtn_date = db.Column(db.Date, nullable=True)
    usta_date = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(255), nullable=True)      # City field
    state = db.Column(db.String(255), nullable=True)     # State field
    country = db.Column(db.String(255), nullable=True)   # Country field
    note = db.Column(db.String(1000), nullable=True)  

    def __repr__(self):
        return '<Player %r>' % self.id