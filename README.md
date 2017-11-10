# Cheap Cruise Finder
Cheap Cruise finder find the cheapest cruise and airfare

## Getting Started
Download and install the latest version of [python3](https://www.python.org/download/releases/3.0/)
### Install python packages
* pip install beautifulsoup4
* pip install Flask
* pip install SQLAlchemy

## How to use
python3 ./runme.py -c <cruise location> -l <flight location>

### Rebuild Documentation 
sphinx-apidoc -o rst/ ../src/
sphinx-build -b html rst/ html/
