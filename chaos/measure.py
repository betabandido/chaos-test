import requests
import statistics
import sys
import time

url = sys.argv[1]
max_latency = float(sys.argv[2])

def make_request():
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Error ocurred: {}'.format(response.status_code))

def time_request():
    t0 = time.perf_counter()
    make_request()
    t = time.perf_counter()

    return (t - t0) * 1000

times = [time_request() for i in range(0, 50)]

if statistics.mean(times) < max_latency:
    print('OK')
else:
    raise Exception('Latency was too high')
