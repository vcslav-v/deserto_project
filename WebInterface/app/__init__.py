from flask import Flask
from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)()
bootstrap = Bootstrap(app)

from app import routes, models