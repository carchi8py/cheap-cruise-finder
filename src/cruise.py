from bs4 import BeautifulSoup
import requests

#To start with i'll hard code 21 (with is hawaiian cruises).
DESTINATION = "21"
PARAMS = {"destination": DESTINATION}
URL = "https://cruises.affordabletours.com/search/advanced_search"

def main():
    cruises = find_search_results()
    # the first cruise row is the header of the table, which we don't care about so we will skip them
    for cruise in cruises[1:]:
        cruise_data = get_cruise_data(cruise)

def get_cruise_data(cruise):
    date = cruise.find("td", {"class": "table-date"}).text
    line = cruise.find("td", {"class": "table-line"}).text
    ship = cruise.find("td", {"class": "table-ship"}).text
    destination = cruise.find("td", {"class": "table-destination"}).text
    departs = cruise.find("td", {"class": "table-departs"}).text
    nights = cruise.find("td", {"class": "table-nights"}).text
    price = cruise.find("td", {"class": "table-price"}).text
    return [date, line, ship, destination, departs, nights, price]

def find_search_results():
    r = requests.get(URL, params=PARAMS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")

if __name__ == "__main__":
    main()
