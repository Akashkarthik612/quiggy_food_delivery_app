from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from config import config   
from db_connection import db
from models import Restaurant, Menu, Order
import datetime
import requests
        
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.route('/ui')
def ui():
    return app.send_static_file('index.html')


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

# Add this import at the top of your app.py
import requests

# Add this route to your app.py file
@app.route('/cart/checkout', methods=['POST'])
def checkout():
    """Process checkout - communicates with cart microservice"""
    try:
        # Get cart data from cart microservice
        cart_response = requests.get('http://127.0.0.1:5001/cart')
        if cart_response.status_code != 200:
            return jsonify({'error': 'Unable to fetch cart'}), 400
        
        cart_data = cart_response.json()
        cart_items = cart_data.get('cart_items', [])
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        data = request.get_json()
        user_id = data.get('user_id', 1)
        
        # Group items by restaurant for order creation
        restaurant_orders = {}
        for item in cart_items:
            restaurant_id = item['restaurant_id']
            if restaurant_id not in restaurant_orders:
                restaurant_orders[restaurant_id] = {
                    'total_quantity': 0,
                    'total_amount': 0,
                    'restaurant_name': item['restaurant_name'],
                    'location': item['location']
                }
            restaurant_orders[restaurant_id]['total_quantity'] += item['quantity']
            restaurant_orders[restaurant_id]['total_amount'] += item['total_amount']
        
        # Create orders in database
        orders_created = []
        total_checkout_amount = 0
        
        for restaurant_id, order_data in restaurant_orders.items():
            order = Order(
                user_id=user_id,
                restaurant_id=restaurant_id,
                order_date=datetime.utcnow(),
                quantity=order_data['total_quantity'],
                total_amount=order_data['total_amount']
            )
            db.session.add(order)
            
            orders_created.append({
                'restaurant_id': restaurant_id,
                'restaurant_name': order_data['restaurant_name'],
                'location': order_data['location'],
                'total_amount': order_data['total_amount']
            })
            
            total_checkout_amount += order_data['total_amount']
        
        # Commit orders to database
        db.session.commit()
        
        # Clear cart in cart microservice
        clear_response = requests.delete('http://127.0.0.1:5001/cart/clear')
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully!',
            'orders_created': orders_created,
            'total_amount': float(total_checkout_amount),
            'order_count': len(orders_created)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Checkout failed: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)