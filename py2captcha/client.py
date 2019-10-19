import time
from collections import namedtuple

from six.moves.urllib_parse import urljoin
from .exceptions import TwoCaptchaException
from bs4 import BeautifulSoup

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session


ServiceLoad = namedtuple('ServiceLoad', [
    'free_workers',  # Amount of idle workers
    'load',  # Service load factor
    'workers_total',  # Amount of workers
    'bid',  # CAPTCHA price
    'speed'  # Average CAPTCHA solve speed
])


class CaptchaJob(object):
    """Class to handle CAPTCHA jobs in the server"""

    def __init__(self, client, task_id):
        """Creates an instance of the class

        Keyword Arguments:
        @param client: The API client
        @type client: TwoCaptchaClient
        @param task_id: The ID of the task. The ID is returned by the server
            when the task is created
        @type task_id: string
        """
        self.client = client
        self.task_id = task_id
        self._last_result = None
        self._last_elapsed_time = None

    def _update(self):
        """Update the status of the task"""
        self._last_result = self.client.get_task_result(self.task_id)

    def check_is_ready(self):
        """Check if a task is complete"""
        self._update()
        return self._last_result['request'] != 'CAPCHA_NOT_READY'

    def get_solution_response(self):
        """Get the solved CAPTCHA"""
        if '|' in self._last_result['request']:
            return self._last_result['request'].split('|')[0]
        else:
            return self._last_result['request']

    def get_solution_cost(self):
        """CAPTCHA solution cost"""
        if '|' in self._last_result['request']:
            return float(self._last_result['request'].split('|')[1]) / 1000
        else:
            return 0.00299

    def get_solution_time(self):
        """CAPTCHA solution time"""
        return self._last_elapsed_time

    def report_bad_captcha(self):
        """Reports a bad CAPTCHA"""
        return self.client.report_bad_captcha(task_id=self.task_id)

    def join(self, maximum_time=300, sleep_time=5):
        """Wait for a CAPTCHA to be solved

        Keyword Arguments:
        @param maximum_time: Maximum time to wait for a CAPTCHA to be solved
        @type maximum_time: int
        @param sleep_time: Sleep time between checks
        @type maximum_time: int
        """
        elapsed_time = 0
        while not self.check_is_ready():
            time.sleep(sleep_time)
            elapsed_time += sleep_time
            if elapsed_time is not None and elapsed_time > maximum_time:
                err_msg = ("The execution time exceeded a "
                           "maximum time of {} seconds.").format(maximum_time)
                raise TwoCaptchaException('TASK_TIMEOUT', err_msg)
        self._last_elapsed_time = elapsed_time


class TwoCaptchaClient(object):
    """2Captcha API client"""

    BALANCE_PARAMS = "&action=getbalance"
    CREATE_TASK_URL = "/in.php"
    TASK_RESULT_URL = "/res.php"
    QUEUE_STATS_URL = "/public_statistics"
    BASE_PARAMS = "?key={0}&json=1"

    def __init__(self, client_key, use_ssl=False):
        """Creates a new instance of the class

        Keyword Arguments:
        @params client_key: 2Captcha API key
        @type client_key: str
        @params use_ssl: Indicates whether to use SSL
        @type use_ssl: bool
        """
        # 2Captcha API key
        self.base_params = self.BASE_PARAMS.format(client_key)

        # Constructing base URL
        proto = "https" if use_ssl else "http"
        self.base_url = "{proto}://2captcha.com/".format(proto=proto)

        # Session instance
        self.session = Session()
        retries = Retry(total=5, backoff_factor=10)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _check_response(self, response):
        if(response.get('status', False) == 0 and
           response.get('request') != "CAPCHA_NOT_READY"):

            raise TwoCaptchaException(
                "CAPTCHA_SOLVE_ERROR",
                response['request']
            )

    def create_task(self, task):
        """Create a CAPTCHA request in the server

        Keyword Arguments:
        @param task: The task to be created on the server
        @type task: BaseTask

        @returns:An object to handle the task created on the server
        @rtype: CaptchaJob
        """
        request = self.base_params + task.serialize()

        response = self.session.post(urljoin(
            urljoin(self.base_url, self.CREATE_TASK_URL), request)
        ).json()

        self._check_response(response)

        return CaptchaJob(self, response['request'])

    def get_task_result(self, task_id):
        """Obtain the result of a CATPCHA request

        Keyword Arguments:
        @param task_id: The ID of the task. The ID is returned by the server
            when the task is created
        @type task_id: string
        @param retries: Number of retries for connection errors
        @type retries: int
        """
        result_params = "&action=get2&id={0}".format(task_id)
        request = self.base_params + result_params

        response = self.session.post(urljoin(
            urljoin(self.base_url, self.TASK_RESULT_URL), request)
        ).json()

        self._check_response(response)

        return response

    def get_balance(self):
        """Get account balance"""
        balance_params = "&action=getbalance"
        request = self.base_params + balance_params

        response = self.session.post(urljoin(
            urljoin(self.base_url, self.TASK_RESULT_URL), request)
        ).json()

        self._check_response(response)

        return response['request']

    def report_bad_captcha(self, task_id):
        """Reports a bad CAPTCHA solution

        Keyword Arguments:
        @param task_id: The ID of the task. The ID is returned by the server
            when the task is created
        @type task_id: string
        """
        report_paramrs = "&action=reportbad&id={0}".format(task_id)
        request = self.base_params.format(self.client_key) + report_paramrs

        response = self.session.post(urljoin(
            urljoin(self.base_url, self.TASK_RESULT_URL), request)
        ).json()

        self._check_response(response)

        return response.get('request') == "OK_REPORT_RECORDED"

    def get_queue_stats(self):
        """Get 2Captcha.com service stats"""
        status_request = self.session.get(urljoin(self.base_url,
                                                  self.QUEUE_STATS_URL))

        if status_request.status_code != 200:
            raise TwoCaptchaException(
                "ERROR_2CAPTCHA_SERVICE",
                "Response status code: %d" % status_request.status_code,
            )

        try:
            # Parse html queue page
            parser_soup = BeautifulSoup(status_request.text, "html.parser")

            # Find cost
            bid_data = parser_soup.find_all(id="market-price")
            if bid_data is not None and len(bid_data) >= 2:
                bid = bid_data[1].get_text()

            # Find average speed
            solving_speed_data = parser_soup.find_all(id="block-size")
            if solving_speed_data is not None and len(solving_speed_data) >= 2:
                solving_speed = solving_speed_data[1].get_text()

            # Find service load
            service_load_data = parser_soup.find_all(id="tx-per-day")
            if service_load_data is not None and len(service_load_data) >= 2:
                service_load = service_load_data[1].get_text()

            # Find service load
            workers_total_data = parser_soup.find_all(id="mempool-size")
            if workers_total_data is not None and len(workers_total_data) >= 2:
                workers_total = workers_total_data[1].get_text()

            service_load = int(service_load.replace('%', ''))
            workers_total = int(workers_total)
            solving_speed = int(solving_speed.replace('s', ''))
            busy_workers = int(workers_total * service_load / 100)
            free_workers = workers_total - busy_workers
            bid = float(bid)

            return ServiceLoad(
                free_workers=free_workers,
                workers_total=workers_total,
                bid=bid,
                load=service_load,
                speed=solving_speed
            )

        except Exception:
            raise TwoCaptchaException(
                "ERROR_2CAPTCHA_SERVICE",
                "Error parsing queue status information"
            )
