"""
https://cruises.affordabletours.com/search/advanced_search/?destination=21&departuredate=&cruiseline1=&numnights=0&dport1=&resident=
"""

from bs4 import BeautifulSoup
import requests

#To start with i'll hard code 21 (with is hawaiian cruises.
DESTINATION = "21"
PARAMS = {"destination": DESTINATION}
URL = "https://cruises.affordabletours.com/search/advanced_search"

def main():
    r = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup)

if __name__ == "__main__":
    main()