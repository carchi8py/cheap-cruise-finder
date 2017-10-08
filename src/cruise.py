from bs4 import BeautifulSoup
import requests
import datetime

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Cruise

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#To start with i'll hard code 21 (with is hawaiian cruises).
DESTINATION = "21"
PARAMS = {"destination": DESTINATION}
URL = "https://cruises.affordabletours.com/search/advanced_search"

def main():
    i = 1
    while i < 10:
        cruises = find_search_results(i)
        # the first cruise row is the header of the table, which we don't care about so we will skip them
        for cruise in cruises[1:]:
            cruise_data = get_cruise_data(cruise)
            add_to_db(cruise_data)
        i+=1

def add_to_db(cruise_data):
    #Check to see if a cruise line exists
    if not session.query(exists().where(CruiseLine.name == cruise_data[1])).scalar():
        add_cruiseline(cruise_data[1])
        print("Adding CruiseLine %s to database" % cruise_data[1])
    if not session.query(exists().where(Ship.name == cruise_data[2])).scalar():
        add_ship(cruise_data[2])
        print("Adding Ship %s to database" % cruise_data[2])
    if not session.query(exists().where(Port.name == cruise_data[4])).scalar():
        add_port(cruise_data[4])
        print("Adding Port %s to database" % cruise_data[4])
    date_obj = datetime.datetime.strptime(cruise_data[0], "%b %d, %Y").date()
    if not session.query(exists().where(Cruise.date == date_obj and \
                                        Cruise.nights == cruise_data[5] and \
                                        Cruise.destination == cruise_data[3])).scalar():
        add_cruise(cruise_data, date_obj)
        print("Adding cruise %s to database" % str(cruise_data))

def add_cruiseline(cruise_line):
    commit(CruiseLine(name = cruise_line))

def add_ship(ship):
    commit(Ship(name = ship))

def add_port(port):
    commit(Port(name = port))

def add_cruise(cruise_data, date_obj):
    line_obj = session.query(CruiseLine).filter_by(name = cruise_data[1]).one()
    ship_obj = session.query(Ship).filter_by(name = cruise_data[2]).one()
    port_obj = session.query(Port).filter_by(name = cruise_data[4]).one()
    new_curise = Cruise(date = date_obj,
                        line = line_obj,
                        ship = ship_obj,
                        destination = cruise_data[3],
                        departs = port_obj,
                        nights = cruise_data[5],
                        price = cruise_data[6])
    commit(new_curise)

def commit(query):
    session.add(query)
    session.commit()

def get_cruise_data(cruise):
    date = cruise.find("td", {"class": "table-date"}).text
    line = cruise.find("td", {"class": "table-line"}).text
    ship = cruise.find("td", {"class": "table-ship"}).text
    destination = cruise.find("td", {"class": "table-destination"}).text
    departs = cruise.find("td", {"class": "table-departs"}).text
    nights = cruise.find("td", {"class": "table-nights"}).text
    price = cruise.find("td", {"class": "table-price"}).text
    return [date, line, ship, destination, departs, nights, price]

def find_search_results(page = 1):
    PARAMS["Page"] = page
    r = requests.get(URL, params=PARAMS)
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")

if __name__ == "__main__":
    main()
