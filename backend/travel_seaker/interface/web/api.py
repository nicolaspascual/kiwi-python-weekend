from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from travel_seaker.db import get_session
from travel_seaker.interface.validation import valid_date
from travel_seaker.models import Journey
from travel_seaker.scrapper import FlixBusScrapper

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search')
@cross_origin()
def search():
    form = request.args

    departure_date_from = valid_date(form.get('departure_date_from'))
    departure_date_to = valid_date(form.get('departure_date_to'))
    source = form.get('source')
    destination = form.get('destination')

    return jsonify(
        [
            t.as_dict()
            for t in FlixBusScrapper().get_trips(
                source,
                destination,
                departure_date_from,
                departure_date_to
            )
        ]
    )


@app.route('/combinations')
@cross_origin()
def combinations():
    form = request.args
    combinations = Journey.get_combinations(
        get_session(),
        form.get('source'),
        form.get('destination'),
        valid_date(form.get('departure_date_from')),
        valid_date(form.get('departure_date_to'))
    )
    singles = FlixBusScrapper().get_trips(
        form.get('source'),
        form.get('destination'),
        valid_date(form.get('departure_date_from')),
        valid_date(form.get('departure_date_to'))
    )
    return jsonify(
        [
            t.as_dict()
            for t in singles
        ] +
        [
            [combination[0].as_dict(), combination[1].as_dict()]
            for combination in combinations
        ]
    )
