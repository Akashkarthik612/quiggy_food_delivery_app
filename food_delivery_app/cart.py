from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from db_connection import db
from models import Restaurant, Menu
import os

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = os.urandom(24)
CORS(app)
db.init_app(app)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart with restaurant_id, menu_name, location, and total_amount"""
    try:
        data = request.get_json()
        
        restaurant_id = data.get('restaurant_id')
        menu_id = data.get('menu_id')
        quantity = data.get('quantity', 1)
        
        if not restaurant_id or not menu_id:
            return jsonify({'error': 'Restaurant ID and Menu ID are required'}), 400
        
        # Get restaurant and menu details
        restaurant = Restaurant.query.get(restaurant_id)
        menu_item = Menu.query.get(menu_id)
        
        if not restaurant or not menu_item:
            return jsonify({'error': 'Restaurant or menu item not found'}), 404
        
        # Initialize cart
        if 'cart' not in session:
            session['cart'] = []
        
        # Check if item exists in cart
        for item in session['cart']:
            if item['menu_id'] == menu_id and item['restaurant_id'] == restaurant_id:
                item['quantity'] += quantity
                item['total_amount'] = item['quantity'] * menu_item.price
                session.modified = True
                return jsonify({'success': True, 'message': 'Item quantity updated in cart'}), 200
        
        # Add new item
        cart_item = {
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant.name,
            'location': restaurant.address,
            'menu_id': menu_id,
            'menu_name': menu_item.menu_name,
            'price_per_item': float(menu_item.price),
            'quantity': quantity,
            'total_amount': float(menu_item.price * quantity)
        }
        
        session['cart'].append(cart_item)
        session.modified = True
        
        return jsonify({
            'success': True, 
            'message': f'{menu_item.menu_name} added to cart',
            'cart_count': len(session['cart'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cart', methods=['GET'])
def get_cart():
    """Get all cart items"""
    if 'cart' not in session:
        session['cart'] = []
    
    cart_total = sum(item['total_amount'] for item in session['cart'])
    
    return jsonify({
        'cart_items': session['cart'],
        'cart_total': float(cart_total),
        'cart_count': len(session['cart'])
    })


@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    """Remove item from cart"""
    try:
        data = request.get_json()
        menu_id = data.get('menu_id')
        restaurant_id = data.get('restaurant_id')
        
        if not menu_id or not restaurant_id:
            return jsonify({'error': 'Menu ID and Restaurant ID required'}), 400
        
        if 'cart' not in session:
            return jsonify({'error': 'Cart is empty'}), 404
        
        # Remove item
        for item in session['cart']:
            if item['menu_id'] == menu_id and item['restaurant_id'] == restaurant_id:
                session['cart'].remove(item)
                session.modified = True
                return jsonify({'success': True, 'message': 'Item removed from cart'}), 200
        
        return jsonify({'error': 'Item not found in cart'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    """Clear entire cart"""
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'Cart cleared'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)