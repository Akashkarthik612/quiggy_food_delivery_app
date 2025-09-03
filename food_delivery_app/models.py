from db_connection import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    restaurant_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(150), nullable = False)
    description = db.Column(db.String(300), nullable = True)
    menus = db.relationship('Menu', backref='restaurant', lazy=True)
class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key = True)
    menu_name =  db.Column(db.String(100), nullable = False)
    description_food = db.Column(db.String(300), nullable = True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    price = db.Column(db.Float, nullable = False)
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    restaurant_id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable = False)
    total_amount = db.Column(db.Float, nullable = False)
    

     
    
    
