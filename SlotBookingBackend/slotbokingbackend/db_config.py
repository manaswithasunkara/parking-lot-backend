# from app import app
# from flaskext.mysql import MySQL

# mysql = MySQL()
 
# # MySQL configurations
# app.config['MYSQL_USER'] = 'manu'
# app.config['MYSQL_PASSWORD'] = '*@Manu2002@*'
# app.config['MYSQL_DB'] = 'parking_reservaton'
# app.config['MYSQL_HOST'] = 'localhost:3300'
# mysql.init_app(app)

from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost:3300'
app.config['MYSQL_USER'] = 'manu'
app.config['MYSQL_PASSWORD'] = '*@Manu2002@*'
app.config['MYSQL_DB'] = 'parking_reservaton'
 
mysql = MySQL(app)