from clients.telegram_client import notify
from database.db import commit_status, add_details
from services.message_builder import build_message
from clients.github_client import extract_latest_commit, fetch
from utils.errors import APIRateLimitedError, NetworkError, APIResponseError
import logging


def run_pipeline():
    try:
        data = fetch()
        latest = extract_latest_commit(data)
        sha = latest['sha']

        if commit_status(sha):
            logging.info("No new commit detected")
        else:
            logging.info(f"New commit detected! Saving")
            inserted = add_details(latest)

            if inserted:
                logging.info("New commit saved successfully")
            else:
                logging.warning("Duplicate commit skipped")

            message = build_message(latest)
            notify(message)
            logging.info(f"New commit saved successfully")

    except APIRateLimitedError as e:
        logging.error(f"Rate limit error: {e}")

    except NetworkError as e:
        logging.error(f"Network error: {e}")

    except APIResponseError as e:
        logging.error(f"API error: {e}")

    except Exception as e:
        logging.exception(f"Unexpected crash: {e}")