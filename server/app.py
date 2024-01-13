from flask import Flask, request, make_response, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from model import db, Hero, Hero_power, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

ma = Marshmallow(app)
api = Api(app)

class HeroSchema(ma.SQLAlchemySchema):
    """
    Schema for Hero model.
    """
    class Meta:
        model = Hero
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    super_name = ma.auto_field()
    strength = ma.auto_field()

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("heroesbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("heroes"),
        }
    )

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)

class PowerSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for Power model.
    """
    class Meta:
        model = Power

    name = ma.auto_field()
    description = ma.auto_field()

power_schema = PowerSchema()
powers_schema = PowerSchema(many=True)

class HeroPowerSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for HeroPower model.
    """
    class Meta:
        model = Hero_power

    strength = ma.auto_field()

    # Add hero and power relationships
    hero = ma.Nested(HeroSchema)
    power = ma.Nested(PowerSchema)

hero_power_schema = HeroPowerSchema()
hero_powers_schema = HeroPowerSchema(many=True)

class Heroes(Resource):

    def get(self):
         heroes = Hero.query.all()
         return make_response(heroes_schema.dump(heroes), 200)
     
api.add_resource(Heroes, '/heroes')

class HeroesByID(Resource):

    def get(self, id):
        hero= Hero.query.filter_by(id=id).first()
        return make_response(hero_schema.dump(hero), 200)
    
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
        powers = Power.query.all()
         
        return make_response(powers_schema.dump(powers), 200)
     
api.add_resource(Powers, '/powers')

# Implemented GET /powers/:id route, handled either existing or non-existing powers, and returned JSON data as specified
class PowersByID(Resource):

    def get(self, id):
        power= Power.query.filter_by(id=id).first()

        return make_response(power_schema.dump(power), 200)
    
    # Implemented PATCH /powers/:id route,and returned JSON data as specified.
    def patch(self, id):
        power= Power.query.filter_by(id=id).first()

        data = request.get_json()
        for attr in data:
            setattr(power,attr,data[attr])

        db.session.add(power)
        db.session.commit()

        return make_response(power_schema.dump(power), 200)

api.add_resource(PowersByID, '/powers/<int:id>')

# Implemented GET /hero_powers route
class HeroPowers(Resource):

    def get(self, id):
        hero_power= Hero_power.query.filter_by(id=id).first()

        return make_response(hero_power_schema.dump(hero_power), 200)
    
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

        return make_response(hero_power_schema.dump(new_hero_power), 201)


api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
         


