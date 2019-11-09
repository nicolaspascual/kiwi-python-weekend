from travel_seaker.scrapper import FlixBusScrapper
from travel_seaker.cli.argument_parser import parse
from pprint import pp

user_arguments = parse()
pp(
    FlixBusScrapper().get_trip(
        user_arguments.source,
        user_arguments.destination,
        user_arguments.departure_date,
    )
)