from app import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)  # 👈 Add this line
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
