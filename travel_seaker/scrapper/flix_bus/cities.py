from requests_html import HTMLSession

from travel_seaker.cache import cache_redis
from travel_seaker.configuration import Configuration


class FlixBusCitiesScrapper(object):

    @property
    def cities(self):
        return self.scrap_cities()
    
    def get_stations_from_city(self, city_name, only_ids=False):
        cities = [
            c['id'] if only_ids else c
            for c in self.cities 
            if city_name.lower() in c['aliases'].split() or\
                city_name.lower() == c['name'].lower()
        ]
        if len(cities) < 1: raise ValueError('The provided city does not exist')
        return cities

    @cache_redis
    def get_city(self, city_name):
        return self.get_stations_from_city(city_name)[0]

    def scrap_cities(self):
        session = HTMLSession()
        raw_json = session.get(Configuration()['flixbus']['cities']['base_url']).json()
        return raw_json['cities'].values()
