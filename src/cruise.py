from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import time
from decimal import Decimal

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
    works = True
    i = 1
    while works:
        try:
            cruises = find_search_results(i)
        except:
            works = False
            continue
        # the first cruise row is the header of the table, which we don't care about so we will skip them
        for cruise in cruises[1:]:
            cruise_data = get_cruise_data(cruise)
            add_to_db(cruise_data)
        i+=1

def add_to_db(cruise_data):
    """
    Add a specific cruise to our database

    :param cruise_data: Should be a list in the following order [date, curise line, Cruise ship, The Destination, the departure port, how many night, the price in USD]
    :return: nothing
    """
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

def remove_from_db(cruise_data):
    """
    Remove a cruise from the database.

    :param cruise_data: Should be a list in the following order [date, curise line, Cruise ship, The Destination, the departure port, how many night, the price in USD]
    :return: nothing
    """
    db_delete(session.query(Cruise).filter_by(nights = cruise_data[5]).first())
    print("Removing Cruise")
    db_delete(session.query(Port).filter_by(name = cruise_data[4]).first())
    print("Removing Port")
    db_delete(session.query(Ship).filter_by(name=cruise_data[2]).first())
    print("Removing Ship")
    db_delete(session.query(CruiseLine).filter_by(name=cruise_data[1]).first())
    print("Removing CruiseLine")


def add_cruiseline(cruise_line):
    """
    commit a cruise Line to the cruise line table in the database

    :param cruise_line: The name of the Cruise line
    :return: nothing
    """
    commit(CruiseLine(name = cruise_line))

def add_ship(ship):
    """
    Commit a cruise ship to the cruise ship table in the database

    :param ship: the name of the cruise ship
    :return: nothing
    """
    commit(Ship(name = ship))

def add_port(port):
    """
    Commis a Port to the Port table in the database

    :param port: The name of the Port
    :return: nothing
    """
    commit(Port(name = port))

def add_cruise(cruise_data, date_obj):
    line_obj = session.query(CruiseLine).filter_by(name = cruise_data[1]).one()
    ship_obj = session.query(Ship).filter_by(name = cruise_data[2]).one()
    port_obj = session.query(Port).filter_by(name = cruise_data[4]).one()
    money_int = int(sub(r'[^\d.]', '', cruise_data[6]))
    new_curise = Cruise(date = date_obj,
                        line = line_obj,
                        ship = ship_obj,
                        destination = cruise_data[3],
                        departs = port_obj,
                        nights = cruise_data[5],
                        price = money_int)
    commit(new_curise)

def commit(query):
    """
    Runs a commit to add data to the database

    :param query: the sqlalchemy add statement we want to run
    :return: nothing
    """
    session.add(query)
    session.commit()

def db_delete(query):
    """
    Runs a delete to remove data from the database

    :param query: the sqlalchemy delete statement we want to run
    :return: nothing
    """
    session.delete(query)
    session.commit()

def get_cruise_data(cruise):
    """
    Parses a single row of the affordable tours cruise search results to get cruise information

    :param cruise: a single html row from the search results
    :return: a list of information on a single cruise
    """
    date = cruise.find("td", {"class": "table-date"}).text
    line = cruise.find("td", {"class": "table-line"}).text
    ship = cruise.find("td", {"class": "table-ship"}).text
    destination = cruise.find("td", {"class": "table-destination"}).text
    departs = cruise.find("td", {"class": "table-departs"}).text
    nights = cruise.find("td", {"class": "table-nights"}).text
    price = cruise.find("td", {"class": "table-price"}).text
    return [date, line, ship, destination, departs, nights, price]

def find_search_results(page = 1):
    """
    Grab the content of affordabletours curise search website and return the search results

    :param page: the number of pages to get
    :return: return the table that contains the search results
    """
    PARAMS["Page"] = page
    r = requests.get(URL, params=PARAMS)
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")

if __name__ == "__main__":
    main()
