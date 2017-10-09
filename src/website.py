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
    # TODO: Show a page that show the different pages we've made

def curiseLines('/lines/'):
    #TODO: show all cruise lines alphabeticly

def ships('/ships/'):
    #TODO: Show all curise ships

def ports('/ports/'):
    #TODO: Show all Ports

def cruiseByPricePreDay('/curises/'):
    #TODO Show all curises by cheapest price pre day


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)