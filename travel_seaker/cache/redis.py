from travel_seaker.configuration import Configuration
from redis import StrictRedis
import pickle

def _get_client():
    return StrictRedis(
        host=Configuration()['redis']['host'],
        port=Configuration()['redis']['port'],
    )

def _construct_key(fn, arguments, kwarguments):
    arguments = arguments[1:] # Get rid of caller self
    redis_key = f'{fn.__name__}'
    if arguments:
        redis_key += f'{arguments}'
    if kwarguments:
        redis_key += f'{kwarguments}'
    return redis_key

def cache_redis(fn):
    client = _get_client()
    def _cache(*arguments, **kwarguments):
        redis_key = _construct_key(fn, arguments, kwarguments)
        if client.exists(redis_key):
            sol = pickle.loads(client.get(redis_key))
        else:
            sol = fn(*arguments, **kwarguments)
            client.setex(
                redis_key,
                Configuration()['redis']['time_invalidate'],
                pickle.dumps(sol)
            )
        return sol
    return _cache