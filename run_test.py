import unittest

from app import create_app, db

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

        #add initial trader and trade
        response = cls.client.post('/api/add_trader', json={'name': 'test_trader'})
        response = cls.client.post('/api/add_trade', json={'currency_pair': 'EURUSD', 'amount': 100, 'price': 1.2, 'trader_id': 1})
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_add_trader(self):
        response = self.client.post('/api/add_trader', json={'name': 'test_trader2'})
        self.assertEqual(response.status_code, 201)
    
    def test_add_trade(self):
        response = self.client.post('/api/add_trade', json={'currency_pair': 'EURUSD', 'amount': 100, 'price': 1.2, 'trader_id': 1})
        self.assertEqual(response.status_code, 201)
    
    def test_get_traders(self):
        response = self.client.get('/api/get_trader?trader_id=1')
        self.assertEqual(response.status_code, 200)

    def test_get_trade(self):
        response = self.client.get('/api/get_trade?trade_id=1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()