'''this script is used to run the food delivery app'''
'''this script initializes the Flask app and sets up the database connection'''
'''the app is configured to use SQLAlchemy for ORM and SQLite as the database'''

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config   
from db_connection import db
from models import Restaurant, Menu, Order

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def home():
    return "Backend is running!"


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    # this route will fetch the results of restaurants from the database
    data = [{'id': r.restaurant_id, 'name': r.name, 'address': r.address, 'description': r.description} 
            for r in restaurants]
    return jsonify(data)


@app.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_restaurant_menu(restaurant_id):
    menu_items = Menu.query.filter_by(restaurant_id=restaurant_id).all()
    data = [{'id': m.id, 'name': m.menu_name, 'description': m.description_food, 'price': m.price} 
            for m in menu_items]
    return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)