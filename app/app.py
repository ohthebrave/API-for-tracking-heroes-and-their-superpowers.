from flask import Flask, jsonify, request, make_response
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from models import db, Hero, Power, Hero_power 
from flask_cors import CORS

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

post_args= reqparse.RequestParser()
post_args.add_argument('id', type=int, required=True)
post_args.add_argument('strength', type=str, required=True)
post_args.add_argument('hero_id', type=int, required=True)
post_args.add_argument('power_id', type=int, required=True)

@app.route('/')
def home():
    return 'This is the home page'

class Heroes(Resource):

    def get(self):
        heroes = Hero.query.all()
        heroes_dict = [
            {
                'id':hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            }
            for hero in heroes
        ]

        return jsonify(heroes_dict)

api.add_resource(Heroes, '/heroes')

# Implemented GET /heroes/:id route, handled either existing or non-existing heroes, and returned JSON data as specified. 
class HeroesByID(Resource):

    def get(self, id):

        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                            "id": hero_power.power.id,
                            "name": hero_power.power.name,
                            "description": hero_power.power.description
                        }
                
                    for hero_power in hero.hero_powers
                ]
            }
            return jsonify(hero_data)
        else:
            response_dict = {"error": "Hero not found"}
            return jsonify(response_dict),404

api.add_resource(HeroesByID, '/heroes/<int:id>')

class PowerResource(Resource):
    def get(self):
        powers = Power.query.all()
        power_dict = [
            {
                "id":power.id,
                "name":power.name,
                "description": power.description,
            }
            for power in powers
        ]
        return jsonify(power_dict)
   
api.add_resource(PowerResource, '/powers')

class PowerById(Resource):
    
     def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(power_data)
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = jsonify(response_dict), 404
            return response

     def patch(self, id):
        data = request.get_json()
        power_input = Power.query.filter_by(id=id).first()

        for attr in data:
          setattr(power_input, attr, data[attr])

        db.session.add(power_input)
        db.session.commit()

        return make_response(power_input.to_dict(), 202)

api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowerResource(Resource):
    def get(self):
        users_dict = [user.to_dict() for user in Hero_power.query.all()]
        return make_response(users_dict, 200)
    
    def post(self):
        data = request.get_json()
        new_user = Hero_power(
                strength = data["strength"],
                hero_id = data["hero_id"],
                power_id = data["power_id"]
              )
        db.session.add(new_user)
        db.session.commit()

        return make_response(new_user.to_dict(), 201)

api.add_resource(HeroPowerResource, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
