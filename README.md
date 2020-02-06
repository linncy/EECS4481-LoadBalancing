# EECS4481-LoadBalancing
This repository provides the kit of the load balancing project for EECS4481 computer security laboratory.

## Scripts
### request_generator.py
It simulates a number of concurrent users sending requests to the web server.
```python3 request_generator.py server_ip redis_ip number_of_concurrent_users interval_in_seconds_between_consequent_requests```

### get_last_50_response_time_statistics.py
Get the average, median, and standard deviation of the reponse time of the last 50 requests.
```python3 et_last_50_response_time_statistics.py redis_ip redis_port(6379)```
