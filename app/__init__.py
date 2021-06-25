from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from flask_cors import CORS,cross_origin



app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://czzjcisk:9sK8aO8K4rCbhNdW3jHBFckanJ_0Uoob@batyr.db.elephantsql.com/czzjcisk'


db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)



from app import routes