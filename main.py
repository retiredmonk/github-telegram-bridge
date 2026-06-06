import logging
import time
from database.db import init_db
from env import get_settings
from services.controller import run_pipeline
from utils.logger import setup_logging
from utils.errors import APIRateLimitedError, NetworkError, APIResponseError

poll_interval = get_settings().POLL_INTERVAL

def main():
    setup_logging()
    init_db()

    try:
        while True:
            try:
                run_pipeline()
            except APIRateLimitedError as e:
                logging.error(f"Rate limit error: {e}")
            except NetworkError as e:
                logging.error(f"Network error: {e}")
            except APIResponseError as e:
                logging.error(f"API error: {e}")
            except Exception as e:
                logging.exception(f"Unexpected crash: {e}")

            logging.info(f"Sleeping for {poll_interval} seconds...\n")
            time.sleep(poll_interval)

    except KeyboardInterrupt:
        logging.info("User triggered shutdown. Shutting down...")


if __name__ == "__main__":
    main()