from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from travel_seaker.configuration import Configuration


def get_session():
    database_url = f'postgresql://{Configuration()["db"]["user"]}:{Configuration()["db"]["password"]}@{Configuration()["db"]["host"]}:{Configuration()["db"]["port"]}/{Configuration()["db"]["database"]}'

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
