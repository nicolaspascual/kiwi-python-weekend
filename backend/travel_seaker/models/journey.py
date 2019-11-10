from datetime import timedelta

from sqlalchemy import FLOAT, TEXT, Column, Integer, Sequence, String, Date
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased

from travel_seaker.cache import cache_redis

Base = declarative_base()


class Journey(Base):
    __tablename__ = 'journeys'  # name of the table
    id = Column(Integer, Sequence('journeys_id'), primary_key=True)

    source = Column(TEXT)
    destination = Column(TEXT)
    departure_datetime = Column(TIMESTAMP)
    arrival_datetime = Column(TIMESTAMP)
    carrier = Column(TEXT)
    vehicle_type = Column(TEXT)
    price = Column(FLOAT)
    currency = Column(String(3))

    def as_dict(self):
        return {
            'departure_time': self.departure_datetime,
            'arrival_time': self.arrival_datetime,
            'source': self.source,
            'destination': self.destination,
            'price': self.price,
            'currency': self.currency,
            'type': self.vehicle_type,
            'carrier': self.carrier
        }

    @classmethod
    @cache_redis
    def get_combinations(self, session, source, destination, departure_date_from, departure_date_to):
        Journey2 = aliased(Journey)
        return session.query(Journey, Journey2)\
            .join(Journey2, Journey.destination == Journey2.source)\
            .filter(
                Journey.source.ilike(f'%{source}%'),
                Journey2.destination.ilike(f'%{destination}%'),
                Journey.arrival_datetime <= Journey2.departure_datetime,
                Journey.departure_datetime.cast(Date) >= departure_date_from.date(),
                Journey.departure_datetime.cast(Date) <= departure_date_to.date(),
        ).all()
