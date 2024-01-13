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
