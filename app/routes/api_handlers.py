import uuid
from flask import request, jsonify, Blueprint
from app.models.models import Trade, Trader
from app import db
from datetime import datetime
from sqlalchemy import or_

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/add_trader', methods=['POST'])
def add_trader():
    data = request.get_json()
    
    required_fields = ['name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if Trader.query.filter_by(name=data['name']).first() is not None:
        return jsonify({'error': 'Trader already exists'}), 400

    new_trader = Trader(name=data['name'])
    try:
        db.session.add(new_trader)
        db.session.commit()
        return jsonify({'message': 'Trader added successfully', 'trader_id': new_trader.trader_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {e}'}), 500


@api_blueprint.route('/api/add_trade', methods=['POST'])
def add_trade():
    data = request.get_json()

    required_fields = ['currency_pair', 'amount', 'price', 'trader_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    trader = Trader.query.get(data['trader_id'])
    if trader is None:
        return jsonify({'error': 'Trader does not exist'}), 400

    identifier = str(uuid.uuid4())

    new_trade = Trade(
        currency_pair=data['currency_pair'],
        amount=data['amount'],
        price=data['price'],
        identifier=identifier,
        trader_id=data['trader_id'],
        trade_date=datetime.utcnow()
    )

    try:
        db.session.add(new_trade)
        db.session.commit()
        return jsonify({'message': 'Trade added successfully', 'trade_id': new_trade.trade_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {e}'}), 500



@api_blueprint.route('/api/get_trader', methods=['GET'])
def get_trader():
    data = request.args

    required_fields = ['name', 'trader_id']
    
    query_conditions = []
    
    if all(field not in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    if 'name' in data:
        query_conditions.append(Trader.name == data['name'])
    if 'trader_id' in data:
        query_conditions.append(Trader.trader_id == data['trader_id'])
    
    trader = Trader.query.filter(or_(*query_conditions)).first()
    if trader is None:
        return jsonify({'error': 'Trader does not exist'}), 400
    return jsonify({'trader_id': trader.trader_id, 'name': trader.name}), 200


#Endpoint to get trades, can query by trade id, or if trader_id is provided, it will return all trades for that trader
@api_blueprint.route('/api/get_trade', methods=['GET'])
def get_trade():
    data = request.args
    #additionally queries can be made by trader id, and trader id and date
    if 'trade_id' in data:
        trade = Trade.query.get(data['trade_id'])
        if trade is None:
            return jsonify({'error': 'Trade does not exist'}), 400
        return jsonify({'trade_id': trade.trade_id, 'currency_pair': trade.currency_pair, 'amount': trade.amount, 'price': trade.price, 'trade_date': trade.trade_date, 'identifier': trade.identifier, 'trader_id': trade.trader_id}), 200
    elif 'date' in data and 'trader_id' in data:
        #return trades for a trader since specified date
        trades = Trade.query.filter(Trade.trade_date > data['date'], Trade.trader_id == data['trader_id']).all()
        if trades is None:
            return jsonify({'error': 'No trades found for trader since specified date'}), 400
        return jsonify([{'trade_id': trade.trade_id, 'currency_pair': trade.currency_pair, 'amount': trade.amount, 'price': trade.price, 'trade_date': trade.trade_date, 'identifier': trade.identifier, 'trader_id': trade.trader_id} for trade in trades]), 200
    elif 'trader_id' in data:
        trades = Trade.query.filter_by(trader_id=data['trader_id']).all()
        if trades is None:
            return jsonify({'error': 'No trades found for trader'}), 400
        return jsonify([{'trade_id': trade.trade_id, 'currency_pair': trade.currency_pair, 'amount': trade.amount, 'price': trade.price, 'trade_date': trade.trade_date, 'identifier': trade.identifier, 'trader_id': trade.trader_id} for trade in trades]), 200
    else:
        return jsonify({'error': 'Missing required fields'}), 400
