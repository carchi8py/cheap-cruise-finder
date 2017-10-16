import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import cruise
from database_setup import Base, CruiseLine, Ship, Port, Cruise

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Cruise variables
FAKE_DATE = "Oct 17, 1990"
FAKE_LINE = "Carchi8py Super curise"
FAKE_SHIP = "The Carchi8py"
FAKE_DESTINATION = "Mars"
FAKE_DEPARTS = "Earth"
FAKE_NIGHTS = "2000"
FAKE_PRICE = "$999,999,999,999"


class testAddCruiseToDatabase(unittest.TestCase):
    def test_adding_to_database(self):
        fake_cruise = [FAKE_DATE, FAKE_LINE, FAKE_SHIP, FAKE_DESTINATION, FAKE_DEPARTS, FAKE_NIGHTS, FAKE_PRICE]
        cruise.add_to_db(fake_cruise)
        test_cruise = session.query(Cruise).filter_by(nights=FAKE_NIGHTS).one()
        self.assertEqual(test_cruise.line.name, FAKE_LINE)
        self.assertEqual(test_cruise.ship.name, FAKE_SHIP)
        self.assertEqual(test_cruise.destination, FAKE_DESTINATION)
        self.assertEqual(test_cruise.departs.name, FAKE_DEPARTS)
        self.assertEqual(test_cruise.nights, int(FAKE_NIGHTS))
        cruise.remove_from_db(fake_cruise)
        test_cruise = session.query(Cruise).filter_by(nights=FAKE_NIGHTS).first()
        self.assertIsNone(test_cruise)
        test_ship = session.query(Ship).filter_by(name=FAKE_SHIP).first()
        self.assertIsNone(test_ship)
        test_line = session.query(CruiseLine).filter_by(name=FAKE_LINE).first()
        self.assertIsNone(test_line)
        test_port = session.query(Port).filter_by(name=FAKE_DEPARTS).first()
        self.assertIsNone(test_port)

if __name__=="__main__":
    unittest.main()