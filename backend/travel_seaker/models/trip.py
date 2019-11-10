from datetime import datetime, timedelta
import re

class Trip(object):
    def __init__(self, departure_datetime, arrival_datetime, source, destination,
                 price, currency, type, source_id, destination_id, free_seats, carrier):
        self.departure_datetime = departure_datetime
        self.arrival_datetime = arrival_datetime
        self.source = source
        self.destination = destination
        self.price = price
        self.currency = currency
        self.type = type
        self.source_id = source_id
        self.destination_id = destination_id
        self.free_seats = free_seats
        self.carrier = carrier

    def as_dict(self):
        return {
            'departure_time': self.departure_datetime,
            'arrival_time': self.arrival_datetime,
            'source': self.source,
            'destination': self.destination,
            'price': self.price,
            'currency': self.currency,
            'type': self.type,
            'source_id': self.source_id,
            'destination_id': self.destination_id,
            'free_seat': self.free_seats,
            'carrier': self.carrier
        }

    def __repr__(self):
        return str(self.as_dict())

    @classmethod
    def from_html_values(cls, departure_date, departure_time, arrival_time, ride_duration,
                 source, destination, price, type, source_id, destination_id, free_seats,
                 carrier):


        departure_datetime = cls.__combine_date_time(departure_date, departure_time)
        arrival_datetime = departure_datetime + timedelta(hours=cls.__parse_ride_duration(ride_duration))
        arrival_datetime = cls.__combine_date_time(arrival_datetime, arrival_time)

        return Trip(
            departure_datetime, arrival_datetime, source, destination,
            *cls.__parse_price(price), type, source_id, destination_id,
            cls.__parse_seats(free_seats), carrier
        )

    @classmethod
    def __combine_date_time(cls, date, time_str):
        return datetime.combine(date, datetime.strptime(time_str,"%H:%M").time())

    @classmethod
    def __parse_ride_duration(cls, ride_duration):
        try:
            return int(re.search(r'\d+', ride_duration)[0])
        except TypeError:
            return 0

    @classmethod
    def __parse_price(cls, price):
        try:
            return float(re.match(r'\d+\.\d+', price)[0]), price[-1]
        except:
            return -1, '?'

    @classmethod
    def __parse_seats(cls, seats):
        try:
            return int(re.match(r'\d+', seats)[0])
        except:
            return None
