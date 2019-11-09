from requests_html import HTMLSession
from travel_seaker.configuration import Configuration
from travel_seaker.models import Trip
import re
from travel_seaker.cache import cache_redis

class FlixBusTripScrapper(object):

    def __init__(self):
        self.session = HTMLSession()
        self.session.get(Configuration()['flixbus']['url'])

    @cache_redis
    def get_trip_information(self, source, destination, departure_date):
        response = self.session.get(
            Configuration()['flixbus']['search']['url'].format(
                departure_date=departure_date,
                source_id=source['id'], destination_id=destination['id'],
                source=source['name'], destination=destination['name']
            )
        )
        return self.scrap_trips(response.html, source, destination, departure_date)

    def scrap_trips(self, response, source, destination, departure_date):
        trips = []
        for raw_html_trip in response.find('.ride-item-pair'):
            trips.append(self.scrap_trip(raw_html_trip, source, destination, departure_date))
        return trips


    def scrap_trip(self, html_trip, source, destination, departure_date):
        return Trip.from_html_values(
            departure_date=departure_date,
            departure_time=html_trip.find(".ride-times .departure", first=True).text,
            arrival_time=html_trip.find('.ride-times .arrival', first=True).text,
            source=html_trip.find('.departure-station-name', first=True).text,
            destination=html_trip.find('.arrival-station-name', first=True).text,
            price=html_trip.find('.currency-small-cents', first=True).text,
            type=html_trip.attrs['data-transport-type'],
            source_id=source['id'],
            destination_id=destination['id'],
            free_seats=html_trip.find('.seats-notice', first=True),
            carrier='flixbus'
        )