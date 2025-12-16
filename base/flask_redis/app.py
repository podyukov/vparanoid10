import time
import redis
import os
from flask import Flask

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'localhost')
cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    return cache.incr('hits')

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
