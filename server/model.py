from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('Hero_power', backref='Hero')

    def __repr__(self):
        return f"<Hero {self.name}, created at {self.created_at}>"
    
class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    hero_id=db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id=db.Column(db.Integer, db.ForeignKey('powers.id'))

    ALLOWED_STRENGTHS= {"Strong", "Weak", "Average"}

    # Validations added to HeroPower model for strength attribute.
    @validates('strength')
    def validate_strength(self, key, value):
        if not value:
            raise ValueError("Must have a strength")
        if len(value) > 20:
            raise ValueError("Strength should not exceed 50 characters")
        if value not in self.ALLOWED_STRENGTHS:
            raise ValueError(f"Invalid description. Allowed values: {', '.join(self.ALLOWED_STRENGTHS)}")
        return value

    def __repr__(self):
        return f"<Hero ({self.id}) of {self.strength}>"

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('Hero_power', backref='Power')

    # Validations added to Power model for description attribute. 
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must not be empty")
        if len(value) > 255:
            raise ValueError("Description should not exceed 255 characters")
        # Allowed values validation (English characters only)
        if not re.match("^[a-zA-Z ]*$", value):
            raise ValueError("Description must contain only English characters.")
        return value 

    def __repr__(self):
        return f"<Power {self.name}: {self.description}>"
