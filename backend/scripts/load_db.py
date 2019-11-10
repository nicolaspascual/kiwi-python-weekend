from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from travel_seaker.configuration import Configuration
from travel_seaker.models import Journey
from travel_seaker.scrapper import FlixBusScrapper

database_url = f'postgresql://{Configuration()["db"]["user"]}:{Configuration()["db"]["password"]}@{Configuration()["db"]["host"]}:{Configuration()["db"]["port"]}/{Configuration()["db"]["database"]}'

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()


session.query(Journey).all()

for c1 in ['Barcelona', 'Madrid', 'Paris', 'London', 'Prague']:
    for c2 in ['Barcelona', 'Madrid', 'Paris', 'London', 'Prague']:
        if c1 != c2:
            print(c1, c2)
            trips = FlixBusScrapper().get_trips(
                c1,
                c2,
                date.today(),
                date.today() + timedelta(days=5),
            )
            for trip in trips:
                journey = Journey(
                    source=trip.source,
                    destination=trip.destination,
                    departure_datetime=trip.departure_datetime,
                    arrival_datetime=trip.arrival_datetime,
                    carrier=trip.carrier,
                    vehicle_type=trip.type,
                    price=trip.price,
                    currency=trip.currency
                )
                session.add(journey)
    session.commit()
