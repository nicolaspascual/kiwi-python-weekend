from requests_html import HTMLSession

from travel_seaker.cache import cache_redis
from travel_seaker.configuration import Configuration
from travel_seaker.models import Trip


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
            departure_time=self.extract_text_from_selector(html_trip, ".ride-times .departure"),
            arrival_time=self.extract_text_from_selector(html_trip, '.ride-times .arrival'),
            ride_duration=self.extract_text_from_selector(html_trip, '.ride__duration'),
            source=self.extract_text_from_selector(html_trip, '.departure-station-name'),
            destination=self.extract_text_from_selector(html_trip, '.arrival-station-name'),
            price=self.extract_text_from_selector(html_trip, '.currency-small-cents'),
            type=html_trip.attrs['data-transport-type'],
            source_id=source['id'],
            destination_id=destination['id'],
            free_seats=self.extract_text_from_selector(html_trip, '.seats-notice'),
            carrier='flixbus'
        )

    def extract_text_from_selector(self, html, selector):
        try:
            return html.find(selector, first=True).text
        except:
            return ''