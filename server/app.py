from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from model import db

from resources import Heroes, HeroPowers, Powers, PowersByID, HeroesByID

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroesByID, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowersByID, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
         


