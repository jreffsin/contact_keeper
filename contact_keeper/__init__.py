from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instantiate Flask
application = Flask(__name__)
# Add Database
# application.config['SQLALCHEMY_DATABASE_URI'] = 'iris://_SYSTEM:sys@localhost:1972/CONTACT_KEEPER'
application.config['SQLALCHEMY_DATABASE_URI'] = 'iris://SuperUser:Z4jf4w78Yd@54.82.61.16:1972/CONTACT_KEEPER'
# Define Secret Key
application.config['SECRET_KEY'] = '38ac236044b43fe5db1a4f7fa466160e'
# Initialize Database
db = SQLAlchemy(application)

from contact_keeper import routes