import argparse
from travel_seaker.interface.validation import valid_date

def parse():
    parser = argparse.ArgumentParser(description='Gt information on buses posted on flixbus')
    parser.add_argument('-s', '--source', type=str, required=True,
                        help='The source to go from')
    parser.add_argument('-d', '--destination', type=str, required=True,
                        help='The destination to go to')
    parser.add_argument('-f', '--departure_date_from', type=valid_date, required=True,
                        help='The date to depart in format "%Y-%m-%d"')
    parser.add_argument('-t', '--departure_date_to', type=valid_date, required=True,
                        help='The date to depart in format "%Y-%m-%d"')
    return parser.parse_args()
