from model import db, Hero, HeroPower, Power
from flask_marshmallow import Marshmallow

from app import app
ma = Marshmallow(app)

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
        model = HeroPower

    strength = ma.auto_field()

    # Add hero and power relationships
    hero = ma.Nested(HeroSchema)
    power = ma.Nested(PowerSchema)

hero_power_schema = HeroPowerSchema()
hero_powers_schema = HeroPowerSchema(many=True)
