# Trade Management System

System built using Python, Flask, SQLite and SQLAlchemy. Additional static frontend shown on home ('/') route. 

## To run
- To build the system, clone the repository and (optional) setup a virtual environment using
```python -m venv venv```
To activate the virtual environment run
```venv\Scripts\activate```
- Install requirements (Flask, SQLAlchemy) with
```pip install -r requirements.txt```
- To run tests, run
```python run_test.py```
This performs all 4 required database executions using the api: Add and Get Trader, and Add and Get Trade
- To build the project, run
```python run.py```
You can interact with the api by referencing the Endpoints section below
## Database
Built using SQLite and SQLAlchemy, the database is created in the initializer in the utilities section, and imported from database.py to avoid circular importing issues. The tables in the database are configured in the app/models/models.py file according to the requirements. By using the model class provided by SQLAlchemy, we can build the tables (along with their internal data types, relationships, and **primary** /  *foreign* keys) as python data structures which can easily interact with both systems. Interaction with the database is all governed by the abstraction layer provided by SQLA. The classes are:

**Trader** (includes backreference from trade object so program can call trade.trader)\
Table name: 'traders'

**trader_id** = Integer\
	name = String(10)

**Trade**\
Table name: 'trades'\
**trade_id** = Integer\
currency_pair = String(10)\
amount  =  Float\
price  =  Float\
trade_date  =  DateTime\
identifier  =  String\
*trader_id*  =  Integer (ForeignKey-> traders.trader_id)

(no columns are nullable for both tables)

## Procedures
Interaction with the database all happens in the routes/api_handlers.py file. Each endpoint has it's own function, which ingests the query information and follows standard response protocol for either adding or reading information from the database. The main functions for database are object based, so we query depending on if we use the Trader or Trade object, these functions are Object.query, and DB.add and .commit. These are built in to SQLA, so instead of using cursors or raw SQL code to INSERT INTO a database, we can use a model and database class. This also helps with checking for common errors like rejecting a trader insert if they already exist, or even breaking down our get requests so we can query differently depending on parameters provided, as shown in the endpoints section.

## Endpoints

- **Add Trader** POST request */api/add_trader* \
Add a new trader to the traders table\
POST

```json
{
	"name" : string
}
```
RESPONSE
Successful (201)
```json
{
  "message": string,
  "trader_id": int
}
```
- **Add Trade** POST request */api/add_trade* \
Add a new trade to the trades table\
POST
```json
{
    "currency_pair": string, 
    "amount": float,
    "price": float,
    "trader_id": int
}
```
RESPONSE
Successful (201)
```json
{
  "message": string,
  "trade_id": int
}
```
- **Get Trader** GET request */api/get_trader* \
Retrieve a trader from the traders table\
Additional functionality to query by either name, trader_id, or both \
GET Query Parameters\
	name : string\
	or\
	trader_id: int\
	or\
	name : string\
	trader_id: int\
RESPONSE
Successful (200)
```json
{
  "name": string,
  "trader_id": int
}
```
- **Get Trade(s)** GET request */api/get_trade* \
Retrieve a trade or multiple trades from the trades table\
Additional functionality to query by:\
	trader id and date: returns list of trades from given trader from specified date\
	trader id: returns list of all trades by given trader\
GET Query Parameters\
	trade_id: int\
	or\
	trader_id: string\
	date: DateTime\
	or\
	trader_id\
RESPONSE
Successful (200)
```json
{
    "currency_pair": string, 
    "amount": float,
    "identifier": UUID (128 bit string - 36 characters),
    "price": float,
    "trader_id": int,
    "trade_id" int,
    "trade_date" DateTime
}
```
or\
Array of trades sorted by trade_date