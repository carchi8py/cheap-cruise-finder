import requests
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

    .. code-block:: json
    
    {
        "mapIdfrom": "las-vegas",
        "duration": {
            "total": 5220,
            "return": 0,
            "departure": 5220
        },
        "flyTo": "SJC",
        "conversion": {
            "USD": 22,
            "EUR": 19
        },
        "deep_link": "https://www.kiwi.com/deep?from=LAS&to=SJC&departure=29-11-2017&flightsId=332966413&price=19&passengers=1&affilid=picky&lang=en&currency=USD&booking_token=TjFsU9KOyjpEDqm5dNSrO5K0FG+q3rKETaHbA5WJ2yQXDnTgCWyBzCSbEggtTNtGqPQE9TDm1pkvplYzuWIbdLa3Ge63TzbPtiiWDE7WRL9ll50gaJwrQoQm3Qiny520+PbXZksFq3TMtBNSyBiWfQ/WJm0+hA7cnvs+mr6vpv7fkHQnZtNAdytvupuH0dEXy9YLI/g25CPYLN/4MUSWw5TQurbiO/Oo2L1VjG5JXVFhBqjM+TW4QS2rsBjG558+OkR6YJbeniEWnCamFvyloR/2z1lEyh+E9vPO3maOdZYhX/gElVWz8IFvETDe43KNq7lUWI07WS0VILHuFrvA7OBMkbamBGF6ST4siC/7zo+INq1m0cv1IIJYuqTfTI2UJnbmU5lmthSzsLsAqui/lkBY7B3X3L8iFk+Ih9a+dgNxYN/UZxbd2AYW02u3zjReO5oIhAFWfbhNF2SaVEwbWQIS1XE9bD59lOfcu2Xa8UB5Ggh7JIgRnaaptXHExQeNGLsOXxzFvP2vZJ4ES/JbsfdihyX5zNqb+K+hEqs1N8xz/oSN2EUiPiYYcLQdPq3mkc44u/YgSRK7/QxFT5Gbx7VM8xY4E2F+b5A6D3Z+LjA=",
        "mapIdto": "san-francisco",
        "nightsInDest": null,
        "airlines": [
        "F9"
        ],
        "id": "332966413",
        "facilitated_booking_available": true,
        "pnr_count": 1,
        "fly_duration": "1h 27m",
        "countryTo": {
            "code": "US",
            "name": "United States"
        },
        "baglimit": {
            "hand_width": null,
            "hand_length": null,
            "hold_weight": 22,
            "hand_height": null,
            "hand_weight": null
        },
        "aTimeUTC": 1511989320,
        "p3": 1,
        "price": 22,
        "type_flights": [
        "lcc"
        ],
        "bags_price": {
            "1": 28,
            "2": 65
        },
        "cityTo": "San Jose",
        "transfers": [],
        "flyFrom": "LAS",
        "dTimeUTC": 1511984100,
        "p2": 1,
        "countryFrom": {
            "code": "US",
            "name": "United States"
        },
        "p1": 1,
        "dTime": 1511955300,
        "found_on": [
        "deprecated"
        ],
        "booking_token": "TjFsU9KOyjpEDqm5dNSrO5K0FG+q3rKETaHbA5WJ2yQXDnTgCWyBzCSbEggtTNtGqPQE9TDm1pkvplYzuWIbdLa3Ge63TzbPtiiWDE7WRL9ll50gaJwrQoQm3Qiny520+PbXZksFq3TMtBNSyBiWfQ/WJm0+hA7cnvs+mr6vpv7fkHQnZtNAdytvupuH0dEXy9YLI/g25CPYLN/4MUSWw5TQurbiO/Oo2L1VjG5JXVFhBqjM+TW4QS2rsBjG558+OkR6YJbeniEWnCamFvyloR/2z1lEyh+E9vPO3maOdZYhX/gElVWz8IFvETDe43KNq7lUWI07WS0VILHuFrvA7OBMkbamBGF6ST4siC/7zo+INq1m0cv1IIJYuqTfTI2UJnbmU5lmthSzsLsAqui/lkBY7B3X3L8iFk+Ih9a+dgNxYN/UZxbd2AYW02u3zjReO5oIhAFWfbhNF2SaVEwbWQIS1XE9bD59lOfcu2Xa8UB5Ggh7JIgRnaaptXHExQeNGLsOXxzFvP2vZJ4ES/JbsfdihyX5zNqb+K+hEqs1N8xz/oSN2EUiPiYYcLQdPq3mkc44u/YgSRK7/QxFT5Gbx7VM8xY4E2F+b5A6D3Z+LjA=",
        "routes": [
            [
                "LAS",
                "SJC"
            ]
        ],
        "cityFrom": "Las Vegas",
        "aTime": 1511960520,
        "route": [
            {
                "bags_recheck_required": false,
                "mapIdfrom": "las-vegas",
                "flight_no": 1127,
                "original_return": 0,
                "lngFrom": -115.172789096832,
                "flyTo": "SJC",
                "guarantee": false,
                "latTo": 37.3625984,
                "source": "deprecated",
                "combination_id": "332966413",
                "id": "332966413",
                "latFrom": 36.1146658358667,
                "lngTo": -121.9290009,
                "dTimeUTC": 1511984100,
                "aTimeUTC": 1511989320,
                "return": 0,
                "price": 1,
                "cityTo": "San Jose",
                "flyFrom": "LAS",
                "mapIdto": "san-francisco",
                "dTime": 1511955300,
                "found_on": "deprecated",
                "airline": "F9",
                "cityFrom": "Las Vegas",
                "aTime": 1511960520
            }
        ],
        "distance": 618.35
    },
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
