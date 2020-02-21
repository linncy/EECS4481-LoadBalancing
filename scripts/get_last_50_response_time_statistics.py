from redis import Redis
import numpy as np
import json
import sys

if len(sys.argv) < 3:
    print('Default values will be used for redis ip and port\n')
    redis_ip = '172.18.0.2'
    port = 6379
else:
    print('Default values have been overwritten.')
    redis_ip = sys.argv[1]
    port = int(sys.argv[2])

redis = Redis(host=redis_ip, port=port)
last_50_logs = [json.loads(item.decode()) for item in redis.lrange('log',0 ,49)]
last_50_response_time = [item[2] for item in last_50_logs]
print('Average: {}'.format(np.mean(last_50_response_time)))
print('Median: {}'.format(np.median(last_50_response_time)))
print('Standard Deviation: {}'.format(np.std(last_50_response_time)))
