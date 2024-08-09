from db import db
from datetime import datetime

class PracticeMatch(db.Model):
    __tablename__ = 'practice_match'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.CHAR(1), nullable=True)
    tennis_id = db.Column(db.Integer, nullable=True)
    player1 = db.Column(db.Integer, nullable=False)
    player2 = db.Column(db.Integer, nullable=False)
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
    team1_serve = db.Column(db.Boolean, nullable=True)
    comments = db.Column(db.String(2000), nullable=True)
