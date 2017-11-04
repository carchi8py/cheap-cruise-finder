from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import time
import random
import sys
import json

from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day, Flight
import db

LOCATION_URL = 'https://locations.skypicker.com/?term="'
LOCATION_URL2 = '"&location_types=airport&limit=1'

FLIGHT_URL1 = "https://api.skypicker.com/flights?flyFrom="
FLIGHT_URL2 = "&to="
FLIGHT_URL3 = "&dateFrom="
FLIGHT_URL4 = "&dateTo="
FLIGHT_URL5 = "&one_per_date=1&curr=USD"

TEST_AIRPORT = "SFO"


def main():
    cruises = db.session.query(Cruise).order_by(Cruise.nights).all()
    for cruise in cruises:
        to_flight = None
        from_flight = None
        start_date = cruise.date
        start_airport = get_airport_code(cruise.departs.name)
        days = cruise.days
        end_airport = get_airport_code(days[len(days) -1 ].port.name)
        end_date = days[len(days) -1 ].date
        if TEST_AIRPORT != start_airport:
            to_flight = generate_flight_url(start_date, TEST_AIRPORT, start_airport)
            to_flight_data = get_flight_details(to_flight)
            add_to_cruise(to_flight_data, cruise)
        if TEST_AIRPORT != end_airport:
            from_flight = generate_flight_url(end_date, end_airport, TEST_AIRPORT)
            from_flight_data = get_flight_details(from_flight)
            add_to_cruise(from_flight_data, cruise)

def add_to_cruise(flight_data, cruise):
    """
    Add a Flight to an existing cruise

    :param flight_data: The flight data
    :param cruise: the cruise data
    :return: nothing
    """
    price = "9999"
    if flight_data != None:
        price = flight_data[0]["price"]
    new_flight = Flight(cost = int(price), cruise = cruise)
    db.session.add(new_flight)
    db.session.commit()

def get_airport_code(location):
    """
    Get an airport code, if not return None

    :param location: Get the airport code from skypicker, if more than one place has the same name, return the first one (more popular)
    :return: The airport code, or none
    """
    location_url = generate_location_url(location)
    r = requests.get(location_url)
    parsed_json = json.loads(r.text)
    if len(parsed_json["locations"]) == 0:
        return None
    return parsed_json["locations"][0]["id"]

def get_flight_details(flight_url):
    """
    Get the flight details

    :param flight_url: The skypicker url we want to get the flight for
    :return: The flight data, or none
    """
    if flight_url == None:
        return None
    r = requests.get(flight_url)
    parsed_json = json.loads(r.text)
    if parsed_json["data"] == []:
        return None
    else:
        return parsed_json["data"]


def generate_location_url(location):
    """
    Get the location URL

    :param location: The location we are looking for
    :return: the Location URL
    """
    if ',' in location:
        location = location.split(',')[0]
    url = LOCATION_URL + location +LOCATION_URL2
    print(url)
    return url

def generate_flight_url(date_obj, from_airport, to_airport):
    """
    Generate the Flight url

    :param date_obj: The date of the flight
    :param from_airport: The airport the flight is leaving from
    :param to_airport: The airport the flight is arriving at
    :return: The url that contain the flight information, or none
    """
    try:
        url = FLIGHT_URL1 + from_airport + FLIGHT_URL2 + to_airport + FLIGHT_URL3
        url = url + date_obj.strftime("%d/%m/%Y") + FLIGHT_URL4
        url = url + date_obj.strftime("%d/%m/%Y") + FLIGHT_URL5
        print(url)
    except:
        return None
    return url

if __name__ == "__main__":
    main()
