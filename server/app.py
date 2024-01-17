from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS


from server.model import db, Hero, Hero_power, Power


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return 'This is the home page'

# Implemented GET /heroes route and returned JSON data as specified. 
class Heroes(Resource):

    def get(self):
         
        heroes = [hero.to_dict() for hero in Hero.query.all()]
        return make_response(jsonify(heroes), 200)
     
api.add_resource(Heroes, '/heroes')

# Implemented GET /heroes/:id route, handled either existing or non-existing heroes, and returned JSON data as specified. 
class HeroesByID(Resource):

    def get(self, id):
        hero= Hero.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(hero), 200)
    
    def delete(self, id):

        record = Hero.query.filter_by(id=id).first()
        
        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "Hero successfully deleted"}

        response = make_response(jsonify(response_dict), 200)

        return response

api.add_resource(HeroesByID, '/heroes/<int:id>')

# Implemented GET /powers route and returned JSON data as specified.
class Powers(Resource):

    def get(self):
        
        powers = [power.to_dict() for power in Power.query.all()]
         
        return make_response(jsonify(powers), 200)
     
api.add_resource(Powers, '/powers')

# Implemented GET /powers/:id route, handled either existing or non-existing powers, and returned JSON data as specified
class PowersByID(Resource):

    def get(self, id):
        power= Power.query.filter_by(id=id).first().to_dict()

        return make_response(jsonify(power), 200)
    
    # Implemented PATCH /powers/:id route,and returned JSON data as specified.
    def patch(self, id):
        power= Power.query.filter_by(id=id).first()

        data = request.get_json()
        for attr in data:
            setattr(power,attr,data[attr])

        db.session.add(power)
        db.session.commit()

        return make_response(jsonify(power.to_dict()), 200)

api.add_resource(PowersByID, '/powers/<int:id>')

# Implemented GET /hero_powers route
class HeroPowers(Resource):

    def get(self):
       
        hero_powers= [hero_power.to_dict() for hero_power in Hero_power.query.all()]

        return make_response(jsonify(hero_powers), 200)
    
    # Implemented POST /hero_powers route, created HeroPower, and returned JSON data as specified.
    def post(self):
        data = request.get_json()

        new_hero_power = Hero_power(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id'],
        )

        db.session.add(new_hero_power)
        db.session.commit()

        return make_response(new_hero_power.to_dict(), 201)


api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
         


