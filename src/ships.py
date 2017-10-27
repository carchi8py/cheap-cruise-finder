from bs4 import BeautifulSoup
import requests
import datetime
from re import sub
import time
import random
import sys

from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day
import db


def main():
    ships = db.session.query(Ship).all()
    for ship in ships[1:]:
        get_ship_info(ship)

def get_ship_info(ship_obj):
    ship_url = create_url(ship_obj)
    r = requests.get(ship_url)
    print(ship_url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        resutls = soup.find("ul", {"class": "medium-block-grid-8"})
        resutls = resutls.findAll("ul")
    except:
        print("Could not find ship %s", ship_obj.name)
        return
    parse_results(resutls, ship_obj)


def parse_results(resutls, ship_obj):
    for each in resutls:
        update = False
        if each.find("h5").text == "Built Year":
            ship_obj.build_year = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Refurbished Year":
            ship_obj.refurbished_year = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Crew":
            ship_obj.crew = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Pax Capacity":
            ship_obj.passagers = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Bars":
            ship_obj.bars = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Pools":
            ship_obj.pools = int(each.find("h3").text)
            update = True
        if each.find("h5").text == "Casinos":
            ship_obj.Casinos = int(each.find("h3").text)
            update = True
        if update == False:
            print(each.find("h5").text)
            print(each.find("h3").text)
        else:
            if not ship_obj:
                continue
            else:
                db.session.add(ship_obj)
                db.session.commit()

def create_url(ship):
    url = "https://cruises.affordabletours.com/"
    line = ship.line.name
    #replace spaces with "_"
    line = line.replace(" ", "_")
    #Add Cruise to the end of the name
    line = line + "_Cruises"
    ship_name = ship.name
    ship_name = ship_name.replace(" ", "_")
    return url + line + "/" + ship_name

if __name__ == "__main__":
    main()