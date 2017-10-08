from bs4 import BeautifulSoup
import requests

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Curise

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#To start with i'll hard code 21 (with is hawaiian cruises).
DESTINATION = "21"
PARAMS = {"destination": DESTINATION}
URL = "https://cruises.affordabletours.com/search/advanced_search"

def main():
    cruises = find_search_results()
    # the first cruise row is the header of the table, which we don't care about so we will skip them
    for cruise in cruises[1:]:
        cruise_data = get_cruise_data(cruise)
        add_to_db(cruise_data)

def add_to_db(cruise_data):
    #Check to see if a curise line exists
    if not session.query(exists().where(CruiseLine.name == cruise_data[1])).scalar():
        add_cruiseline(cruise_data[1])
        print("Adding %s to database" % cruise_data[1])

def add_cruiseline(cruise_line):
    new_cruiseline = CruiseLine(name = cruise_line)
    session.add(new_cruiseline)
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

def find_search_results():
    r = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")

if __name__ == "__main__":
    main()
