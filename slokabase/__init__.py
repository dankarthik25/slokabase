from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
import os

from .SqliteModel import get_create_table_query, get_insert_query, get_read_query, get_update_query, get_delete_query
from .SqliteModel import SqliteModel


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

