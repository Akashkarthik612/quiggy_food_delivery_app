# seed.py
from app import app, db
from models import Restaurant, Menu

with app.app_context():
    # Create tables first
    db.create_all()
    
    # Clear existing data
    Restaurant.query.delete()
    Menu.query.delete()
    db.session.commit()
    
    # Create 50 restaurants
    restaurants_data = [
        ("Pizza Palace", "Downtown", "Best pizza in town"),
        ("Burger Barn", "City Center", "Gourmet burgers"),
        ("Sushi Zen", "Riverside", "Authentic Japanese sushi"),
        ("Taco Fiesta", "Main Street", "Authentic Mexican cuisine"),
        ("The Italian Corner", "Little Italy", "Traditional Italian dishes"),
        ("Dragon Wok", "Chinatown", "Authentic Chinese stir-fry"),
        ("Mediterranean Delight", "Harbor View", "Fresh Mediterranean flavors"),
        ("BBQ Smokehouse", "West End", "Slow-cooked barbecue specialties"),
        ("Thai Paradise", "Garden District", "Spicy Thai classics"),
        ("French Bistro", "Old Town", "Classic French cuisine"),
        ("Indian Spice House", "Spice Quarter", "Aromatic Indian curries"),
        ("Greek Taverna", "Seaside", "Traditional Greek dishes"),
        ("Korean Kitchen", "Korea Town", "Authentic Korean BBQ"),
        ("Lebanese Garden", "Cedar Hills", "Fresh Middle Eastern cuisine"),
        ("Vietnamese Pho House", "Little Saigon", "Traditional Vietnamese pho"),
        ("Brazilian Churrasco", "Latin Quarter", "All-you-can-eat grilled meats"),
        ("Ethiopian Flavors", "Cultural District", "Traditional Ethiopian cuisine"),
        ("Peruvian Grill", "South Valley", "Authentic Peruvian dishes"),
        ("Russian Tea Room", "Heritage Square", "Traditional Russian cuisine"),
        ("Moroccan Nights", "Desert View", "Exotic Moroccan tagines"),
        ("Cuban Cafe", "Tropical Avenue", "Authentic Cuban sandwiches"),
        ("German Beer Hall", "Oktoberfest Street", "Traditional German sausages"),
        ("Irish Pub & Grill", "Emerald District", "Hearty Irish comfort food"),
        ("Scottish Highlands", "Highland Park", "Traditional Scottish fare"),
        ("Spanish Tapas Bar", "Flamenco Street", "Authentic Spanish tapas"),
        ("Turkish Delight", "Bosphorus Lane", "Traditional Turkish kebabs"),
        ("Polish Kitchen", "Warsaw Avenue", "Hearty Polish comfort food"),
        ("Ukrainian Home", "Sunflower Street", "Traditional Ukrainian dishes"),
        ("Hungarian Goulash", "Budapest Boulevard", "Authentic Hungarian stews"),
        ("Czech Beer Garden", "Prague Plaza", "Traditional Czech cuisine"),
        ("Argentine Steakhouse", "Tango Street", "Premium Argentine beef"),
        ("Chilean Wine Bar", "Vineyard Row", "Chilean wines and cuisine"),
        ("Colombian Coffee House", "Coffee Bean Lane", "Colombian specialties"),
        ("Jamaican Jerk Hut", "Reggae Road", "Spicy Jamaican jerk chicken"),
        ("Cajun Bayou", "Swamp Street", "Authentic Louisiana Cajun"),
        ("Southern Comfort", "Magnolia Avenue", "Classic Southern cuisine"),
        ("New England Seafood", "Harbor Street", "Fresh New England seafood"),
        ("California Fresh", "Sunset Boulevard", "Fresh California cuisine"),
        ("Texas Smokehouse", "Lone Star Lane", "Authentic Texas BBQ"),
        ("Hawaiian Luau", "Paradise Drive", "Traditional Hawaiian plates"),
        ("Alaskan Salmon Lodge", "Glacier Street", "Fresh Alaskan seafood"),
        ("Florida Keys Fish", "Coral Reef Road", "Fresh Florida seafood"),
        ("New York Deli", "Broadway Street", "Classic New York deli"),
        ("Chicago Deep Dish", "Windy City Avenue", "Authentic Chicago pizza"),
        ("Philadelphia Cheesesteak", "Liberty Street", "Authentic Philly cheesesteaks"),
        ("Boston Chowder House", "Freedom Trail", "New England clam chowder"),
        ("Seattle Coffee Roasters", "Pike Place", "Artisan coffee and pastries"),
        ("Portland Food Truck", "Food Cart Lane", "Gourmet food truck cuisine"),
        ("Denver Mountain Grill", "Rocky Road", "Mountain-inspired cuisine"),
        ("Miami Beach Cafe", "Ocean Drive", "Fresh tropical cuisine")
    ]
    
    restaurants = []
    for name, address, description in restaurants_data:
        restaurant = Restaurant(name=name, address=address, description=description)
        restaurants.append(restaurant)
    
    db.session.add_all(restaurants)
    db.session.commit()
    
    # Refresh all restaurants to get their IDs
    for restaurant in restaurants:
        db.session.refresh(restaurant)
    
    # Create menu items for each restaurant (2-4 items per restaurant)
    menu_items = []
    
    # Menu items for different restaurant types
    menu_templates = {
        "Pizza": [
            ("Margherita Pizza", "Classic tomato and mozzarella", 12.99),
            ("Pepperoni Pizza", "Pepperoni with cheese", 14.99),
            ("Supreme Pizza", "Loaded with toppings", 16.99),
            ("Hawaiian Pizza", "Ham and pineapple", 13.99)
        ],
        "Burger": [
            ("Classic Cheeseburger", "Beef patty with cheese", 8.99),
            ("Bacon Burger", "Beef patty with crispy bacon", 10.99),
            ("Veggie Burger", "Plant-based patty", 9.49),
            ("BBQ Burger", "BBQ sauce and onion rings", 11.99)
        ],
        "Sushi": [
            ("California Roll", "Crab, avocado, cucumber", 8.99),
            ("Salmon Nigiri", "Fresh salmon over rice", 12.99),
            ("Tuna Sashimi", "Fresh tuna slices", 15.99),
            ("Rainbow Roll", "Mixed fish and avocado", 18.99)
        ],
        "Taco": [
            ("Beef Tacos", "Ground beef with toppings", 9.99),
            ("Chicken Tacos", "Grilled chicken with salsa", 9.99),
            ("Fish Tacos", "Grilled fish with cabbage", 11.99),
            ("Veggie Tacos", "Black beans and vegetables", 8.99)
        ],
        "Generic": [
            ("House Special", "Chef's signature dish", 16.99),
            ("Daily Soup", "Fresh soup of the day", 6.99),
            ("Mixed Salad", "Fresh seasonal greens", 8.99),
            ("Grilled Chicken", "Marinated grilled chicken", 14.99)
        ]
    }
    
    # Assign menu items based on restaurant type
    for i, restaurant in enumerate(restaurants):
        restaurant_name = restaurant.name.lower()
        
        if "pizza" in restaurant_name:
            selected_items = menu_templates["Pizza"]
        elif "burger" in restaurant_name:
            selected_items = menu_templates["Burger"]
        elif "sushi" in restaurant_name:
            selected_items = menu_templates["Sushi"]
        elif "taco" in restaurant_name:
            selected_items = menu_templates["Taco"]
        else:
            selected_items = menu_templates["Generic"]
        
        # Add 2-3 menu items per restaurant
        for j, (item_name, description, price) in enumerate(selected_items[:3]):
            menu_item = Menu(
                restaurant_id=restaurant.restaurant_id,
                menu_name=item_name,
                description_food=description,
                price=price
            )
            menu_items.append(menu_item)
    
    db.session.add_all(menu_items)
    db.session.commit()
    
    print(f"Successfully inserted {len(restaurants)} restaurants and {len(menu_items)} menu items!")
    print("Sample restaurants created:")
    for i, restaurant in enumerate(restaurants[:5]):
        print(f"  {i+1}. {restaurant.name} - {restaurant.address}")
    print(f"  ... and {len(restaurants)-5} more restaurants")