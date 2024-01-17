#!/usr/bin/env python3
import random
from app import app
from server.models import db, Hero, Hero_power, Power


with app.app_context():

    Hero.query.delete()
    Hero_power.query.delete()
    Power.query.delete()

    # puts "🦸‍♀️ Seeding powers..."
    heroes_data= [
        { 'name': "Kamala Khan", 'super_name': "Ms. Marvel" },
        { 'name': "Doreen Green", 'super_name': "Squirrel Girl" },
        { 'name': "Gwen Stacy", 'super_name': "Spider-Gwen" },
        { 'name': "Janet Van Dyne", 'super_name': "The Wasp" },
        { 'name': "Wanda Maximoff", 'super_name': "Scarlet Witch" },
        { 'name': "Carol Danvers", 'super_name': "Captain Marvel" },
        { 'name': "Jean Grey", 'super_name': "Dark Phoenix" },
        { 'name': "Ororo Munroe", 'super_name': "Storm" },
        { 'name': "Kitty Pryde", 'super_name': "Shadowcat" },
        { 'name': "Elektra Natchios", 'super_name': "Elektra" }
    ]

    for hero_data in heroes_data:
        hero = Hero(**hero_data)
        db.session.add(hero)

    db.session.commit()

    powers_data = [
        { 'name': "super strength", 'description': "gives the wielder super-human strengths" },
        { 'name': "flight", 'description': "gives the wielder the ability to fly through the skies at supersonic speed" },
        { 'name': "super human senses", 'description': "allows the wielder to use her senses at a super-human level" },
        { 'name': "elasticity", 'description': "can stretch the human body to extreme lengths" }
    ]

    for power_data in powers_data:
        power = Power(**power_data)
        db.session.add(power)

    db.session.commit()

    strengths = ["Strong", "Weak", "Average"]

    # Iterate through each hero
    for hero in Hero.query.all():
        # Choose a random number of powers (1 to 3)
        for _ in range(random.randint(1, 3)):
            # Get a random power from the database
            power = Power.query.get(random.choice(Power.query.with_entities(Power.id).all()[0]))

            # Create a HeroPower instance and add it to the database session
            hero_power = Hero_power(
                hero_id=hero.id,
                power_id=power.id,
                strength=random.choice(strengths)
            )
            db.session.add(hero_power)

    # Commit changes to the database
    db.session.commit()

