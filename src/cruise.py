from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import sys

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Cruise

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

DESTINATIONS = ["21", "10", "2"]
URL = "https://cruises.affordabletours.com/search/advanced_search"
INFO_URL = "https://cruises.affordabletours.com/search/itsd/cruises/"

def main():
    for destination in DESTINATIONS:
        works = True
        i = 1
        params = {"destination": destination}
        while works:
            try:
                cruises = find_search_results(i, params)
            except:
                works = False
                continue
            # the first cruise row is the header of the table, which we don't care about so we will skip them
            for cruise in cruises[1:]:
                cruise_data = get_cruise_data(cruise)
                add_to_db(cruise_data)
                itinerary = get_crusie_info(cruise_data)
                parse_days(itinerary)
                sys.exit(1)
            i+=1

def add_to_db(cruise_data):
    """
    Add a specific cruise to our database

    :param cruise_data: Should be a list in the following order [date, curise line, Cruise ship, The Destination, the departure port, how many night, the price in USD, cruiseid]
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
    if not session.query(exists().where(Cruise.id == int(cruise_data[7]))).scalar():
        add_cruise(cruise_data, date_obj)
        print("Adding cruise %s to database" % str(cruise_data))

def remove_from_db(cruise_data):
    """
    Remove a cruise from the database.

    :param cruise_data: Should be a list in the following order [date, curise line, Cruise ship, The Destination, the departure port, how many night, the price in USD, cruiseid]
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
    """
    Add a specific cruise, line, ship, and port to our database

    :param cruise_data: The Cruise object [date, curise line, Cruise ship, The Destination, the departure port, how many night, the price in USD, cruiseid]
    :param date_obj: The date of the curise
    :return: nothing
    """
    line_obj = session.query(CruiseLine).filter_by(name = cruise_data[1]).one()
    ship_obj = session.query(Ship).filter_by(name = cruise_data[2]).one()
    port_obj = session.query(Port).filter_by(name = cruise_data[4]).one()
    money_int = int(sub(r'[^\d.]', '', cruise_data[6]))
    new_curise = Cruise(id = cruise_data[7],
                        date = date_obj,
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
    k = cruise.find("td", {"class": "table-date"})
    id = k.find("a")["href"].split("cruises/")[1].split('/')[0]
    date = cruise.find("td", {"class": "table-date"}).text
    line = cruise.find("td", {"class": "table-line"}).text
    ship = cruise.find("td", {"class": "table-ship"}).text
    destination = cruise.find("td", {"class": "table-destination"}).text
    departs = cruise.find("td", {"class": "table-departs"}).text
    nights = cruise.find("td", {"class": "table-nights"}).text
    price = cruise.find("td", {"class": "table-price"}).text
    return [date, line, ship, destination, departs, nights, price, id]

def parse_days(itinerary):
    i = 1
    for each in itinerary[1:]:
        days = each.findAll("td")
        date = days[0].text.split(":")[1]
        port = days[1].text.split(":")[1]
        arriavl = days[2].text.split(":",1)[1]
        departure = days[3].text.split(":",1)[1]
        print(date)
        print(port)
        print(arriavl)
        print(departure)

def find_search_results(page, params):
    """
    Grab the content of affordabletours curise search website and return the search results

    :param page: the number of pages to get
    :param params: the params we want to pass to the URL
    :return: return the table that contains the search results
    """
    params["Page"] = page
    r = requests.get(URL, params=params)
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")

def get_crusie_info(data):
    id = data[7]
    r = requests.get(INFO_URL + str(id))
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"id": "maintable"})
    return results.findAll("tr")


if __name__ == "__main__":
    main()
