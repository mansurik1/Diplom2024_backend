import redis
import json

try:
    redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)
except redis.exceptions.ConnectionError:
    print('Redis is not available')

def redis_save_data(key, value, expire=600):
    allowed_types = [float, int, str, bytes]
    if type(value) not in allowed_types:
        value = json.dumps(value)
    redis_cli.setex(key, expire, value)

def redis_get_data(key):
    data = redis_cli.get(key)
    if data:

        return data.decode('utf-8')
    else:

        return None
