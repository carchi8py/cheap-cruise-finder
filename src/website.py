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
    new_cruises = []
    for cruise in cruises:
        total_price = cruise.price
        for flight in cruise.flights:
            total_price += flight.cost
        cruise.total = total_price
        if len(cruise.flights) == 0:
            cruise.flight1 = "N/A"
            cruise.flight2 = "N/A"
        elif len(cruise.flights) == 1:
            cruise.flight1 = cruise.flights[0].cost
            cruise.flight2 = "N/A"
        else:
            cruise.flight1 = cruise.flights[0].cost
            cruise.flight2 = cruise.flights[1].cost
        new_cruises.append(cruise)
    return render_template('cruise.html', cruises=new_cruises)

@app.route('/days/')
def cruise_days():
    days = session.query(Day)
    return render_template('day.html', days=days)

@app.route('/itinerary/<id>')
def cruise_itinerary(id):
    days = session.query(Day).filter_by(cruise_id = id)
    return render_template('day.html', days=days)

@app.route("/ships/<id>")
def ship_info(id):
    ship = session.query(Ship).filter_by(id = id)
    return render_template('ship.html', ships=ship)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)