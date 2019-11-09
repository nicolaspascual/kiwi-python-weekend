from travel_seaker.configuration import Configuration
from requests_html import HTMLSession
from .cities import FlixBusCitiesScrapper
from .trips import FlixBusTripScrapper

class FlixBusScrapper(object):

    def __init__(self):
        self.cities = FlixBusCitiesScrapper()
        self.trips = FlixBusTripScrapper()

    def get_trip(self, source, destination, departure_date):
        source = self.cities.get_city(source)
        destination = self.cities.get_city(destination)
        return self.trips.get_trip_information(
            source,
            destination,
            departure_date
        )