
import cruise
import ships
import flights
import argparse
import sys

CRUISE_HELP = """The following is the mapping of cruise on Affordable tours
    1. Africa
    2. Alaska -- All
    3. Alaska -- Gulf of Alaska
    4. Alaska -- Inside Passage
    5. Antarctica
    6. Asia
    25. Australia/ New Zealand
    7. Bahamas
    12. Baltic
    8. Bermuda
    28. Black Sea
    9. Canada
    10. Caribbean -- All
    11. Caribbean -- Eastern
    12. Caribbean -- Southern
    13. Caribbean -- Western
    14. Central America
    37. Cruise to Nowhere
    39. Cuba
    16. Europe -- All
    18. Europe -- Northern
    19. Europe -- Western
    20. Greek Isles
    21. Hawaii
    17. Mediterranean
    31. Mexico
    36. Middle East
    22. Panama Canal
    24. South America
    34. Tahiti
    26. Transatlantic
    27. USA -- All
    33. USA -- New England
    28. USA -- Pacific
    39. USA -- SouthEast
    30. World Cruise
    """

def main(argv):
    """

    :return:
    """
    options = _parse_options(argv)
    cruise.main(options.cruise)
    ships.main()
    flights.main(options.location)

def _parse_options(argv):
    parser = argparse.ArgumentParser(argv, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--cruise", dest="cruise", default="21",
                        help = CRUISE_HELP)
    parser.add_argument("-l", "--location", dest="location", default="San Francisco",
                        help = "String contains the location you need fights from. Example: 'San Francisco'")
    return parser.parse_args()

if __name__ == "__main__":
    main(sys.argv)