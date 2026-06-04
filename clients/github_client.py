import requests
import logging
import time
import random
from env import get_settings
from utils.errors import APIResponseError, APIRateLimitedError, NetworkError

def fetch ():

    config = get_settings()

    headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {config.GITHUB_TOKEN}',
    'User-Agent': 'github-telegram-bridge/1.0'
    }

    user = config.OWNER
    repo = config.REPO

    params = {
        "per_page": 5
    }

    url = f"https://api.github.com/repos/{user}/{repo}/commits"

    max_retries, base = 3, 2

    saw_rate_limit = False
    saw_network_error = False
    saw_server_error = False

    for attempt in range(1, max_retries+1):

        wait = random.uniform (0, base *2 ** attempt)

        try:
            response = requests.get(url, headers=headers, params= params, timeout=10.0)

            if response.status_code == 403:
                saw_rate_limit = True
                logging.warning(f'Too many requests, sleeping for {wait} seconds')
                time.sleep(wait)
                continue

            if 500 <= response.status_code <= 599:
                saw_server_error = True
                logging.warning(f"Server error: {response.status_code}")
                time.sleep(wait)
                continue

            data = response.json()

            logging.info("Latest Commit Fetched Successfully")
            return data


        except requests.exceptions.RequestException as e:
            logging.warning(f"Network error: {e}. Retrying in {wait}s for (attempt {attempt})")
            time.sleep(wait)
            saw_network_error = True

        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise APIResponseError(f"Data validation error: {e}")

        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            raise APIResponseError(f"Unexpected error: {e}")


    if saw_rate_limit:
        logging.error("Rate limit reached, maximum retries reached")
        raise APIRateLimitedError("Rate limit reached, maximum retries reached")

    elif saw_network_error:
        logging.critical("Network error occurred")
        raise NetworkError("Network error occurred")

    elif saw_server_error:
        logging.error("Server error occurred, maximum retries reached")
        raise NetworkError("Failed to connect to server, maximum retries reached")

    else:
        logging.critical("API failed after maximum retries")
        raise APIResponseError("Failed to retrieve data after maximum retries")


def extract_latest_commit(data: list) -> dict:
    if not data:
        raise APIResponseError("Empty commit list from GitHub API")
    return data[0]