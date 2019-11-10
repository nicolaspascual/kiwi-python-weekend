from requests_html import HTMLSession

from travel_seaker.configuration import Configuration

from .cities import FlixBusCitiesScrapper
from .trips import FlixBusTripScrapper

from datetime import timedelta


class FlixBusScrapper(object):

    def __init__(self):
        self.cities = FlixBusCitiesScrapper()
        self.trips = FlixBusTripScrapper()

    def get_trips(self, source, destination, departure_date_from, departure_date_to):
        source = self.cities.get_city(source)
        destination = self.cities.get_city(destination)

        trips = []
        date = departure_date_from
        while date <= departure_date_to:
            trips += self.trips.get_trip_information(
                source,
                destination,
                date
            )
            date += timedelta(days=1)
        return trips
