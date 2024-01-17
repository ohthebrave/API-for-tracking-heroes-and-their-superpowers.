#!/usr/bin/env python3

from app import app
from models import db, Hero, Hero_power, Power


heroes=[{
        "id": 1,
        "name": "Cly",
        "super_name": "Webberley"
        }, {
        "id": 2,
        "name": "Stu",
        "super_name": "Birkmyre"
        }, {
        "id": 3,
        "name": "Waldon",
        "super_name": "Thews"
        }, {
        "id": 4,
        "name": "Keefer",
        "super_name": "O'Henecan"
        }, {
        "id": 5,
        "name": "Win",
        "super_name": "Tadman"
        }, {
        "id": 6,
        "name": "Griswold",
        "super_name": "Weber"
        }, {
        "id": 7,
        "name": "Haily",
        "super_name": "Josefs"
        }, {
        "id": 8,
        "name": "Jessa",
        "super_name": "Muggleston"
        }, {
        "id": 9,
        "name": "Chaim",
        "super_name": "Tandy"
        }, {
        "id": 10,
        "name": "Wells",
        "super_name": "Cogar"
        }]

powers = [{
  "id": 1,
  "name": "Kaile",
  "description": "Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl."
}, {
  "id": 2,
  "name": "Josi",
  "description": "In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet."
}, {
  "id": 3,
  "name": "Sherlock",
  "description": "Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae."
}, {
  "id": 4,
  "name": "Feodora",
  "description": "Fusce consequat. Nulla nisl. Nunc nisl.\n\nDuis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus."
}, {
  "id": 5,
  "name": "Scot",
  "description": "Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede."
}, {
  "id": 6,
  "name": "Jordon",
  "description": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem."
}, {
  "id": 7,
  "name": "Corrianne",
  "description": "Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi."
}, {
  "id": 8,
  "name": "Scarlet",
  "description": "Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra."
}, {
  "id": 9,
  "name": "Cob",
  "description": "Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae.  suscipit a, feugiat et, eros."
}, {
  "id": 10,
  "name": "Helaina",
  "description": "Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh.\n\nIn quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet."
}]

heroPowers =[{
  "id": 1,
  "strength": "Strong",
  "hero_id": 2,
  "power_id": 6
}, {
  "id": 2,
  "strength": "Weak",
  "hero_id": 9,
  "power_id": 1
}, {
  "id": 3,
  "strength": "Strong",
  "hero_id": 7,
  "power_id": 3
}, {
  "id": 4,
  "strength": "Average",
  "hero_id": 6,
  "power_id": 5
}, {
  "id": 5,
  "strength": "Average",
  "hero_id": 4,
  "power_id": 8
}, {
  "id": 6,
  "strength": "Strong",
  "hero_id": 3,
  "power_id": 9
}, {
  "id": 7,
  "strength": "Average",
  "hero_id": 1,
  "power_id": 2
}, {
  "id": 8,
  "strength": "Weak",
  "hero_id": 10,
  "power_id": 7
}, {
  "id": 9,
  "strength": "Average",
  "hero_id": 5,
  "power_id": 4
}, {
  "id": 10,
  "strength": "Weak",
  "hero_id": 8,
  "power_id": 10
}]

with app.app_context():

    db.session.add_all([Hero(**hero) for  hero in heroes])
    db.session.commit()

    # db.session.add_all([Power(**power) for power in powers])
    # db.session.commit()

    # db.session.add_all([Hero_power(**heroPower) for heroPower in heroPowers])
    # db.session.commit()

    