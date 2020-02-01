"""
HTTP Request Generator.  It simulates a number of concurrent users sending requests to the web server.
"""

from redis import Redis
import requests
import json
import time
import threading
import sys

if len(sys.argv) < 4:
    print('To few arguments; you need to specify 3 arguments.')
    print('Default values will be used for server_ip, redis_ip, number of users and interval.\n')
    server_ip = '127.0.0.1'  # ip address of the web server. Default value is localhost
    redis_ip = '172.18.0.2'
    no_users = 1  # number of concurrent users sending request to the web server
    interval = 1  # interval in seconds between consequent requests
else:
    print('Default values have been overwritten.')
    server_ip = sys.argv[1]
    redis_ip = sys.argv[2]
    no_users = int(sys.argv[3])
    interval = float(sys.argv[4])


class HTTPThread(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name + str(self.counter))
        send_request(self.name + str(self.counter))


def send_request(user):
    while True:
        start_time = time.time()
        try:
            r = requests.get('http://' + server_ip + ':8000/', timeout=60)
            data = r.json()
        except requests.exceptions.RequestException as e:
            print(e)
            redis.lpush('errorlog', json.dumps([start_time, str(e)]))
            continue
        end_time = time.time()
        response_time = end_time - start_time
        time.sleep(interval)
        redis.lpush('log', json.dumps([start_time, data['Request_Count'], response_time, data['Compute_Time'], data['Container_Name']]))
        print("Response Time for {} = {}; Response JSON: {}".format(user, response_time, data))


if __name__ == "__main__":
    redis = Redis(host=redis_ip, port=6379)
    threads = []
    for i in range(no_users):
        threads.append(HTTPThread("User", i))

    for i in range(no_users):
        threads[i].start()

    for i in range(no_users):
        threads[i].join()