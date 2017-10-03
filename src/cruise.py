"""
https://cruises.affordabletours.com/search/advanced_search/?destination=21&departuredate=&cruiseline1=&numnights=0&dport1=&resident=
"""

from bs4 import BeautifulSoup
import requests
import sys

#To start with i'll hard code 21 (with is hawaiian cruises.
DESTINATION = "21"
PARAMS = {"destination": DESTINATION}
URL = "https://cruises.affordabletours.com/search/advanced_search"

def main():
    r = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    cruises = results.findAll("tr")
    # the first cruise row is the header of the table, which we don't care about so we will skip them
    for cruise in cruises[1:]:
        date = cruise.find("td", {"class": "table-date"}).text
        line = cruise.find("td", {"class": "table-line"}).text
        ship = cruise.find("td", {"class": "table-ship"}).text
        destination = cruise.find("td", {"class": "table-destination"}).text
        departs = cruise.find("td", {"class": "table-departs"}).text
        nights = cruise.find("td", {"class": "table-nights"}).text
        price = cruise.find("td", {"class": "table-price"}).text
        print(date, line, ship, destination, departs, nights, price)

if __name__ == "__main__":
    main()
