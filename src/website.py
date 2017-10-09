from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Curise
import sys

app = Flask(__name__)

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    #TODO: Show a page that show the different pages we've made
    return

@app.route('/lines/')
def curiseLines():
    lines = session.query(CruiseLine).order_by(CruiseLine.name)
    return render_template('lines.html', lines=lines)

@app.route('/ships/')
def ships():
    #TODO: Show all curise ships
    return

@app.route('/ports/')
def ports():
    #TODO: Show all Ports
    return

@app.route('/curises/')
def cruiseByPricePreDay():
    #TODO Show all curises by cheapest price pre day
    return


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)