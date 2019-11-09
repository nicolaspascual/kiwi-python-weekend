import argparse
from datetime import datetime

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def parse():
    parser = argparse.ArgumentParser(description='Gt information on buses posted on flixbus')
    parser.add_argument('-s', '--source', type=str, required=True,
                        help='The source to go from')
    parser.add_argument('-d', '--destination', type=str, required=True,
                        help='The destination to go to')
    parser.add_argument('-t', '--departure_date', type=valid_date, required=True,
                        help='The date to depart in format "%Y-%m-%d"')
    return parser.parse_args()