from app.database import db
from datetime import datetime

class Trader(db.Model):
    __tablename__ = 'traders'

    trader_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    trades = db.relationship('Trade', backref='trader', lazy=True)

    def __repr__(self):
        return f'<Trader {self.name}>'
    
class Trade(db.Model):
    __tablename__ = 'trades'

    trade_id = db.Column(db.Integer, primary_key=True)
    currency_pair = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    trade_date = db.Column(db.DateTime, nullable=False)
    identifier = db.Column(db.String, unique = True, nullable=False)
    trader_id = db.Column(db.Integer, db.ForeignKey('traders.trader_id'), nullable=False)

    def __repr__(self):
        return f'<Trade {self.trade_id} - {self.currency_pair}>'