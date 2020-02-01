"""
a simple Flask web application with a compute-intensive workload;
return the number of requests it has received and the amount of time it took to solve the compute-intensive workload
difficulty can be changed by defining the environmental variable FACTORIAL, default is 20000
"""

from flask import Flask
from redis import Redis
import time
import json
import os

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
try:
    difficulty = int(os.environ['FACTORIAL'])
except:
    difficulty = 20000

try:
    hostname = os.environ['HOSTNAME']
except:
    hostname = 'NA'

def factorials(n = difficulty):
    result = 1
    start_time = time.time()
    for i in range(1, n+1):
        result *= i
    end_time = time.time()
    compute_time = end_time - start_time
    return compute_time

@app.route('/')
def index():
    request_timestamp = time.time()
    count = redis.incr('requests', amount=1)
    compute_time = factorials()
    redis.lpush('log', json.dumps([count, request_timestamp, compute_time]))
    return json.dumps({'Request_Count': count, 'Compute_Time': compute_time, 'Container_Name':hostname})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)