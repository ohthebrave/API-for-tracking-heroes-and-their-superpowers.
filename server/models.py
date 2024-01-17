from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('Hero_power', back_populates='hero')


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-hero_powers.power')

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('Hero_power', back_populates='power')

class Hero_power(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-hero.powers', '-power.heroes')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    # Hero_power instances are associated with a Hero instance through the hero_powers attribute in the Hero model.
    hero = db.relationship('Hero', back_populates='hero_powers')  

    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    # Hero_power instances are associated with a Power instance through the hero_powers attribute in the Power model.
    power = db.relationship('Power', back_populates='hero_powers')  
