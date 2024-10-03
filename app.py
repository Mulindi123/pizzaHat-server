from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Restaurant, Pizza, RestaurantPizza

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#develppment configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api =Api(app)
CORS(app, origins="*")

class Index(Resource):
    def get(self):
        return make_response(jsonify("Pizza App"))
    
api.add_resource(Index, "/")


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()

        restaurants_list = []
        for restaurant in restaurants:
            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address     
            }

            restaurants_list.append(restaurant_dict)

        response = make_response(jsonify(restaurants_list), 200)

        response.headers["Content-Type"] = "application/json"

        return response

api.add_resource(Restaurants, "/restaurants", endpoint="restaurants")

class RestaurantByID(Resource):
    def get(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:

            restaurant_dict = restaurant.to_dict()
        
            response =  make_response(jsonify(restaurant_dict), 200)
        else:
            response =  make_response({"error": "Restaurant not found"}, 404)

        return response
    
    def delete(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            associated_pizzas = RestaurantPizza.query.filter_by(restaurant_id = id).all()
            for pizza in associated_pizzas:

                db.session.delete(pizza)
                db.session.commit()

            db.session.delete(restaurant)
            db.session.commit()

            return make_response({}, 204)
        
        else:
            response = make_response({"error": "Restaurant not found"}, 404)
            return response
    
api.add_resource(RestaurantByID, "/restaurants/<int:id>", endpoint="restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()

        pizzas_list = []
        for pizza in pizzas:
            pizza_dict = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients     
            }

            pizzas_list.append(pizza_dict)

        return make_response(jsonify(pizzas_list), 200)

api.add_resource(Pizzas, "/pizzas", endpoint="pizzas")

class RestaurantPizzas(Resource):

    def get(self):
        restaurant_pizzas = RestaurantPizza.query.all()

        pizzas_list = []
        for restaurant_pizza in restaurant_pizzas:
            pizza = Pizza.query.get(restaurant_pizza.pizza_id)
            restaurant = Restaurant.query.get(restaurant_pizza.restaurant_id)

            if pizza and restaurant:

                pizza_dict = {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients     
                }

                pizzas_list.append(pizza_dict)

        return make_response(jsonify(pizzas_list), 200) 
    
    def post(self):
        data = request.get_json()

        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        if not price and pizza_id and restaurant_id:
            
            return make_response({"error":"All parameters (price, pizza_id , restaurant_id) are required!"}, 400)
        
        #check if pizza and restaurant exist

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            return make_response({"error":"pizza or restaurant not found."}, 404)
        
        #create a RestaurantPizza record
        restaurant_pizza = RestaurantPizza(
            price = price,
            pizza_id = pizza_id,
            restaurant_id = restaurant_id
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        related_pizza = Pizza.query.get(pizza_id)
        if related_pizza:
            related_pizza_dict = {
                "id": related_pizza.id,
                "name": related_pizza.name,
                "ingredients": related_pizza.ingredients     
            }

            return make_response(jsonify(related_pizza_dict), 201)
        
        return make_response({"error": "Related pizza not found"}, 404)

api.add_resource(RestaurantPizzas, "/restaurant_pizzas", endpoint="restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
