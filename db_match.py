from db import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'match'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duration = db.Column(db.Integer, nullable=True)
    location = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date, nullable=True)
    type = db.Column(db.CHAR(1), nullable=True)
    player1 = db.Column(db.Integer, nullable=True)
    player2 = db.Column(db.Integer, nullable=True)
    player3 = db.Column(db.Integer, nullable=True)
    player4 = db.Column(db.Integer, nullable=True)
    team1_set1 = db.Column(db.Integer, nullable=True)
    team1_set1_tb = db.Column(db.Integer, nullable=True)
    team2_set1 = db.Column(db.Integer, nullable=True)
    team2_set1_tb = db.Column(db.Integer, nullable=True)
    team1_set2 = db.Column(db.Integer, nullable=True)
    team1_set2_tb = db.Column(db.Integer, nullable=True)
    team2_set2 = db.Column(db.Integer, nullable=True)
    team2_set2_tb = db.Column(db.Integer, nullable=True)
    team1_set3 = db.Column(db.Integer, nullable=True)
    team1_set3_tb = db.Column(db.Integer, nullable=True)
    team2_set3 = db.Column(db.Integer, nullable=True)
    team2_set3_tb = db.Column(db.Integer, nullable=True)
    team1_won = db.Column(db.Boolean, nullable=True)
    match_name = db.Column(db.String(200), nullable=True)
    match_level = db.Column(db.String(200), nullable=True)
    match_link = db.Column(db.String(200), nullable=True)
    match_event = db.Column(db.String(200), nullable=True)
    match_draw = db.Column(db.String(200), nullable=True)
    match_round = db.Column(db.String(200), nullable=True)
    match_city = db.Column(db.String(200), nullable=True)
    match_state = db.Column(db.String(200), nullable=True)
    is_indoor = db.Column(db.Boolean, nullable=True)
    comments = db.Column(db.String(2000), nullable=True)
    tennis_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Match %r>' % self.id