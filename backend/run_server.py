from travel_seaker.interface.web import app
from travel_seaker.configuration import Configuration

app.run(
    host=Configuration()['api']['host'],
    port=Configuration()['api']['port'],
    debug=True
)