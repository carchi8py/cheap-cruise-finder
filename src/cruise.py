from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import sys
import time
import random

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

DESTINATIONS = ["21"]
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
                itinerary = get_crusie_info(cruise_data[7])
                parse_days(itinerary, cruise_data[7])
                #So we do hit the site to hard let wait some where between 1 and 20 seconds
                #time.sleep(random.randint(1,10))
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
        add_ship(cruise_data[2], cruise_data[1])
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

def remove_day(day_items):
    days = session.query(Day).filter_by(day=day_items[0])
    for day in days:
        db_delete(day)
        print("Removed day")


def add_cruiseline(cruise_line):
    """
    commit a cruise Line to the cruise line table in the database

    :param cruise_line: The name of the Cruise line
    :return: nothing
    """
    commit(CruiseLine(name = cruise_line))

def add_ship(ship, line):
    """
    Commit a cruise ship to the cruise ship table in the database

    :param ship: the name of the cruise ship
    :param line: the curise line that own the ship
    :return: nothing
    """
    line_obj = session.query(CruiseLine).filter_by(name = line).one()
    commit(Ship(name = ship, line = line_obj))

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

def add_day(day_items):
    curise_obj = session.query(Cruise).filter_by(id=day_items[5]).one()
    if 0 < session.query(Day).filter_by(day = day_items[0], cruise = curise_obj).count():
        return
    arrival_time = None
    departure_time = None
    if not session.query(exists().where(Port.name == day_items[2])).scalar():
        print("Adding port %s " % day_items[2])
        add_port(day_items[2])
    port_obj = session.query(Port).filter_by(name=day_items[2]).one()
    date_obj = datetime.datetime.strptime(day_items[1], "%b %d, %Y").date()
    if "---" not in day_items[3]:
        arrival_time = format_time(day_items[3])
    if "---" not in day_items[4]:
        departure_time = format_time(day_items[4])
    new_day = Day(day = day_items[0],
                  date = date_obj,
                  port = port_obj,
                  cruise = curise_obj)
    commit(new_day)
    update_day = session.query(Day).filter_by(day=day_items[0], cruise=curise_obj).one()
    if arrival_time:
        update_day.arrival = arrival_time
    if departure_time:
        update_day.Departure = departure_time
    commit(update_day)

def format_time(unformatted_time):
    """
    Sanitize the times we get from the website so python can understand them

    :param unformatted_time: the unformated times
    :return: the formated times.
    """
    #Python hour format require a lead zero so, 1:00am become 01:00AM
    if len(unformatted_time.split(":")[0]) == 1:
        unformatted_time = "0" + unformatted_time
    #They use P.M. python time formating wants PM
    unformatted_time = unformatted_time.replace(".", "")
    #even though there using a 12 hour clock they sometime use 00 for 12:00am
    unformatted_time = unformatted_time.replace("00:", "12:")
    #Sometime they print Noon instead of 12:00 pm"
    if unformatted_time == "Noon":
        unformatted_time = "12:00 pm"
    return datetime.datetime.strptime(unformatted_time, "%I:%M %p").time()


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

def parse_days(itinerary, curise_id):
    """
    Parse each day in a cruise itinerary.

    :param itinerary: The Cruise's itinerary in HTML format
    :param curise_id: The Cruise_id so that we can create a ForeignKey relation
    :return: nothing
    """
    i = 1
    for each in itinerary[1:]:
        days = each.findAll("td")
        #For some cruise lines (like  Viking Cruises) they use a different format, i'll skip these
        if len(days) < 4:
            return
        date = days[0].text.split(":")[1]
        port = days[1].text.split(":")[1]
        arrival = days[2].text.split(":",1)[1]
        departure = days[3].text.split(":",1)[1]
        try:
            add_day([i, date, port, arrival, departure, curise_id])
        except:
            print("Couldn't add cruise")
        i += 1

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

def get_crusie_info(cruise_id):
    """
    Grab the content of a specific cruise from affordable tours website

    :param cruise_id: The cruise ID to grab data from
    :return: The table that contains the cruise itinerary
    """
    r = requests.get(INFO_URL + str(cruise_id))
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"id": "maintable"})
    return results.findAll("tr")


if __name__ == "__main__":
    main()
