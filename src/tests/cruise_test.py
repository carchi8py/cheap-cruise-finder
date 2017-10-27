import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import cruise
from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day
import db


#Fake Cruise variables
FAKE_DATE = "Oct 17, 1990"
FAKE_LINE = "Carchi8py Super curise"
FAKE_SHIP = "Azamara_Journey"
FAKE_DESTINATION = "Mars"
FAKE_DEPARTS = "Earth"
FAKE_NIGHTS = "2000"
FAKE_PRICE = "$999,999,999,999"
FAKE_CRUISE_ID = 1

FAKE_DAY = 12303
FAKE_ARRIVAL = "9:00 A.M."
FORMATED_FAKE_ARRIVAL = "09:00:00"
FAKE_DEPARTS_DAY = "Noon"
FORMATED_FAKE_DEPARTS_DAY = "12:00:00"

class testAddCruiseToDatabase(unittest.TestCase):
    def test_adding_to_database(self):
        fake_cruise = [FAKE_DATE, FAKE_LINE, FAKE_SHIP, FAKE_DESTINATION, FAKE_DEPARTS, FAKE_NIGHTS, FAKE_PRICE, FAKE_CRUISE_ID]
        cruise.add_to_db(fake_cruise)
        test_cruise = db.session.query(Cruise).filter_by(nights=FAKE_NIGHTS).one()
        self.assertEqual(test_cruise.line.name, FAKE_LINE)
        self.assertEqual(test_cruise.ship.name, FAKE_SHIP)
        self.assertEqual(test_cruise.destination, FAKE_DESTINATION)
        self.assertEqual(test_cruise.departs.name, FAKE_DEPARTS)
        self.assertEqual(test_cruise.nights, int(FAKE_NIGHTS))
        #Before we remove Cruise we need to add a day and see if it there, then remove it
        self.add_day()
        cruise.remove_from_db(fake_cruise)
        test_cruise = db.session.query(Cruise).filter_by(nights=FAKE_NIGHTS).first()
        self.assertIsNone(test_cruise)
        test_ship = db.session.query(Ship).filter_by(name=FAKE_SHIP).first()
        self.assertIsNone(test_ship)
        test_line = db.session.query(CruiseLine).filter_by(name=FAKE_LINE).first()
        self.assertIsNone(test_line)
        test_port = db.session.query(Port).filter_by(name=FAKE_DEPARTS).first()
        self.assertIsNone(test_port)

    def add_day(self):
        fake_day = [FAKE_DAY, FAKE_DATE, FAKE_DEPARTS, FAKE_ARRIVAL, FAKE_DEPARTS_DAY, FAKE_CRUISE_ID]
        cruise.add_day(fake_day)
        test_day = db.session.query(Day).filter_by(day=FAKE_DAY).one()
        self.assertEqual(test_day.cruise_id, FAKE_CRUISE_ID)
        self.assertEqual(test_day.day, FAKE_DAY)
        self.assertEqual(test_day.port.name, FAKE_DEPARTS)
        self.assertEqual(str(test_day.arrival), FORMATED_FAKE_ARRIVAL)
        self.assertEqual(str(test_day.Departure), FORMATED_FAKE_DEPARTS_DAY)
        cruise.remove_day(fake_day)
        test_day = db.session.query(Day).filter_by(day=FAKE_DAY).first()
        self.assertIsNone(test_day)

if __name__=="__main__":
    unittest.main()