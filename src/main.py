"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


## GET REQUESTS FOR PAGES WITH LISTS OF ITEMS ## 

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()

    all_users = list(map(lambda u: u.serialize(), users))
    
    return jsonify(all_users), 200

@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.all()

    all_characters = list(map(lambda c: c.serialize(), characters))
    
    return jsonify(all_characters), 200

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()

    all_Planets = list(map(lambda p: p.serialize(), planets))
    
    return jsonify(all_Planets), 200


@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()

    all_Vehicles = list(map(lambda p: p.serialize(), vehicles))
    
    return jsonify(all_Vehicles), 200

## GET REQUESTS FOR PAGES WITH SPECIFIC ITEMS ## 

@app.route('/user/<int:id>/', methods=['GET'])
def get_a_user(id):
    user = User.query.get(id)
    a_user = user.serialize()
    return jsonify(a_user), 200

@app.route('/character/<int:id>/', methods=['GET'])
def get_a_character(id):
    character = Character.query.get(id)
    a_character = character.serialize()
    return jsonify(a_character), 200

@app.route('/planet/<int:id>/', methods=['GET'])
def get_a_planet(id):
    planet = Planet.query.get(id)
    a_planet = planet.serialize()
    return jsonify(a_planet), 200


@app.route('/vehicle/<int:id>/', methods=['GET'])
def get_a_vehicle(id):
    vehicle = Vehicle.query.get(id)
    a_vehicle = vehicle.serialize()
    return jsonify(a_vehicle), 200


## POST REQUESTS ## 







# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
