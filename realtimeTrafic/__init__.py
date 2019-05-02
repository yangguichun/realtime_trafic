from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask('realtimetrafic')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:00@127.0.0.1/realtime_trafic'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:00@192.168.1.77/realtime_trafic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from realtimeTrafic import commands, models, views
