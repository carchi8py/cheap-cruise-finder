from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import time
import random
import sys
import json

from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day
import db

LOCATION_URL = 'https://locations.skypicker.com/?term="'
LOCATION_URL2 = '"&location_types=airport&limit=1'

def get_airport_code(location):
    location_url = generate_location_url(location)
    r = requests.get(location_url)
    parsed_json = json.loads(r.text)
    if len(parsed_json["locations"]) == 0:
        return None
    return parsed_json["locations"][0]["id"]


def generate_location_url(location):
    url = LOCATION_URL + location +LOCATION_URL2
    return url

if __name__ == "__main__":
    print(get_airport_code("San Francisco"))
