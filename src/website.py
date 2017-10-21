from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day

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
def curise_lines():
    lines = session.query(CruiseLine).order_by(CruiseLine.name)
    return render_template('lines.html', lines=lines)

@app.route('/ships/')
def ships():
    ships = session.query(Ship).order_by(Ship.name)
    return render_template('ship.html', ships=ships)

@app.route('/ports/')
def ports():
    ships = session.query(Port).order_by(Port.name)
    return render_template('ship.html', ships=ships)

@app.route('/cruises/')
def cruise_by_price_pre_day():
    cruises = session.query(Cruise).order_by(Cruise.price/Cruise.nights)
    return render_template('cruise.html', cruises=cruises)

@app.route('/days/')
def cruise_days():
    days = session.query(Day)
    return render_template('day.html', days=days)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)