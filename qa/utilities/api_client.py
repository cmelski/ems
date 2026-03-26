import requests
import time
from qa.utilities.logging_utils import logger_utility

MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds between retries


class APIClient:
    def __init__(self, base_url, token: str = None):
        self.base_url = base_url
        self.session = requests.session()
        if token:
            self.session.headers.update({'token': token})

    def call_api_with_retry(self, endpoint: str, method: str = "GET", **kwargs) -> requests.Response:
        """
        Makes an API call and retries up to MAX_RETRIES times if the error
        status code is NOT in the 400s (i.e., retries on 5xx or connection errors).
        """
        last_exception = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger_utility().info(f'Endpoint: {self.base_url+endpoint}')
                logger_utility().info(f'Method: {method}')
                response = requests.request(method, self.base_url+endpoint, **kwargs)

                # If status is in 400s (client error), do NOT retry — fail immediately
                if 400 <= response.status_code < 500:
                    logger_utility().error(f"[Attempt {attempt}] Client error {response.status_code} — not retrying.")
                    return response

                # If successful (2xx/3xx), return immediately
                if response.status_code < 400:
                    logger_utility().info(f"[Attempt {attempt}] Success: {response.status_code}")
                    return response

                # 5xx or other non-400 errors — retry
                logger_utility().warning(f"[Attempt {attempt}] Server error {response.status_code} — retrying...")

            except requests.exceptions.RequestException as e:
                last_exception = e
                logger_utility().warning(f"[Attempt {attempt}] Request failed: {e} — retrying...")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        # Exhausted all retries
        if last_exception:
            raise last_exception

        return response  # Return last response even if it was a server error
