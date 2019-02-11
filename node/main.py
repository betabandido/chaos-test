import logging
import os
import requests
import time

from flask import abort, Flask
from circuitbreaker import circuit

app = Flask(__name__)


@circuit(failure_threshold=5)
def make_request(url):
    for _ in range(0, 3):
        try:
            logging.info('Making request to {}'.format(url))
            response = requests.get(url, timeout=0.2)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logging.error('Error making request: {}'.format(e))

        logging.warning('Waiting for 0.1s')
        time.sleep(0.2)

    raise Exception('Timed-out')


@app.route('/')
def do():
    content = '.'

    next_node = os.environ.get('CHAOS_TEST_NEXT_NODE')
    if next_node is not None:
        try:
            content += make_request(next_node)
        except Exception as e:
            logging.error('Error fetching data from next node: {}'.format(e))

    return content


@app.route('/healthz')
def healthz():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
