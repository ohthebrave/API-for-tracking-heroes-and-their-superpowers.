from flask import Flask,jsonify,make_response,request
from flask_migrate import Migrate
from flask_restful import Api, Resource,reqparse
from flask_cors import CORS


from models import db, Hero, Hero_power,Power


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

post_args= reqparse.RequestParser()
# post_args.add_argument('id', type=int, required=True)
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
    def post(self):
        data = request.get_json()

        # Extract data from the request
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        # Check if power and hero exist
        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if power is None or hero is None:
            return jsonify({'error': 'Power or Hero not found'}), 404

        # Create a new HeroPower instance
        hero_power = Hero_power(strength=strength, hero=hero, power=power)

        # Add and commit to the database
        db.session.add(hero_power)
        db.session.commit()

        # Manual serialization
        serialized_hero_power = {
            'id': hero_power.id,
            'strength': hero_power.strength,
            'hero': {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            },
            'power': {
                'id': power.id,
                'name': power.name,
                'description': power.description
            },
            'created_at': hero_power.created_at,
            'updated_at': hero_power.updated_at
        }

        return jsonify(serialized_hero_power), 201
   
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
        power = Power.query.filter_by(id=id).first()
        if power:
            data = request.get_json()
            description = data.get('description')
            power.description = description
            db.session.commit()

            response = {
                "id":power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(response)
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = jsonify(response_dict)
            return response

api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowerResource(Resource):

    def post(self):
        data = post_args.parse_args()

        # Check if the specified hero and power exist
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])

        if not hero or not power:
            return jsonify({'error': 'Hero or Power not found'}), 404

        # Create a new HeroPower instance
        new_hero_power = Hero_power(
            strength=data['strength'],
            hero=hero,
            power=power
        )

        db.session.add(new_hero_power)
        db.session.commit()

        return jsonify(new_hero_power.to_dict()), 201 

api.add_resource(HeroPowerResource, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
         


