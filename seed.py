from faker import Faker
from random import randint, choice as rc
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():

    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    for _ in range(5):
        restaurant = Restaurant(
            name=fake.company(),
            address = fake.address()
        )
        
        restaurants.append(restaurant)
    db.session.add_all(restaurants)




    pizzas =[]

    pizza_list = [
    {"name": "Margherita", "ingredients": "Tomato sauce, Mozzarella cheese, Fresh basil, Olive oil, Salt"},
    {"name": "Pepperoni", "ingredients": "Tomato sauce, Mozzarella cheese, Pepperoni slices"},
    {"name": "Vegetarian", "ingredients": "Tomato sauce, Mozzarella cheese, Bell peppers, Mushrooms, Onions, Olives"},
    {"name": "Hawaiian", "ingredients": "Tomato sauce, Mozzarella cheese, Ham, Pineapple"},
    {"name": "BBQ Chicken", "ingredients": "BBQ sauce, Mozzarella cheese, Grilled chicken, Red onions, Cilantro"},
    {"name": "Supreme", "ingredients": "Tomato sauce, Mozzarella cheese, Pepperoni, Sausage, Bell peppers, Onions, Olives, Mushrooms"},
    {"name": "White Pizza", "ingredients": "Olive oil, Mozzarella cheese, Ricotta cheese, Garlic, Spinach, Parmesan cheese"},
    {"name": "Mushroom Truffle", "ingredients": "Truffle oil, Mozzarella cheese, Mushrooms, Garlic, Thyme, Parmesan cheese"},
    {"name": "Buffalo Chicken", "ingredients": "Buffalo sauce, Mozzarella cheese, Grilled chicken, Red onions, Cilantro, Blue cheese dressing"},
    {"name": "Meat Lovers", "ingredients": "Tomato sauce, Mozzarella cheese, Pepperoni, Sausage, Bacon, Ground beef"},
]
    for data in pizza_list:
        pizza = Pizza(name = data["name"],ingredients = data["ingredients"])

        pizzas.append(pizza)
    db.session.add_all(pizzas)
   
    restaurant = Restaurant.query.all()
    pizza = Pizza.query.all()

    restaurant_pizzas =[]
    for restaurant in restaurants:
        for _ in range(3):
            pizza = rc(pizzas)
            price = randint(1, 30)
            restaurant_pizza = RestaurantPizza(
                restaurant_id= restaurant.id,
                pizza_id =pizza.id,
                price=price
            )

            print(f"Adding restaurant_pizza: {restaurant_pizza}")
            
            restaurant_pizzas.append(restaurant_pizza)
    db.session.add_all(restaurant_pizzas)

    db.session.commit()

    try:
        db.session.commit()
    except Exception as e:
        print(f"An error occurred during commit: {e}")

    restaurant = Restaurant.query.all()
    pizza = Pizza.query.all()

   