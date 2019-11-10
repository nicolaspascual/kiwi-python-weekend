from travel_seaker.scrapper import FlixBusScrapper
from travel_seaker.interface.cli.argument_parser import parse
from pprint import pp

user_arguments = parse()
pp(
    FlixBusScrapper().get_trips(
        user_arguments.source,
        user_arguments.destination,
        user_arguments.departure_date_from,
        user_arguments.departure_date_to,
    )
)