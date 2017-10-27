import os
import sys
import unittest
from bs4 import BeautifulSoup
import requests


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import ships, cruise
import db
from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day


#Fake Cruise variables
FAKE_DATE = "Oct 17, 1990"
FAKE_LINE = "Carchi8py Super curise"
FAKE_SHIP = "Azamara_Journey"
FAKE_DESTINATION = "Mars"
FAKE_DEPARTS = "Earth"
FAKE_NIGHTS = "2000"
FAKE_PRICE = "$999,999,999,999"
FAKE_CRUISE_ID = 1

class testAddShipInfoToDatabase(unittest.TestCase):
    def test_adding_info(self):
        url = "https://cruises.affordabletours.com/Azamara_Club_Cruises/Azamara_Journey/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        resutls = soup.find("ul", {"class": "medium-block-grid-8"})
        resutls = resutls.findAll("ul")

        fake_cruise = [FAKE_DATE, FAKE_LINE, FAKE_SHIP, FAKE_DESTINATION, FAKE_DEPARTS, FAKE_NIGHTS, FAKE_PRICE, FAKE_CRUISE_ID]
        cruise.add_to_db(fake_cruise)
        test_ship = db.session.query(Ship).filter_by(name=FAKE_SHIP).first()
        ships.parse_results(resutls, test_ship)

if __name__=="__main__":
    unittest.main()
