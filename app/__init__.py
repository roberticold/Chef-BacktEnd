from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from flask_cors import CORS,cross_origin



app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///productss.db'


db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)



from app import routes