import logging
from clients.github_client import fetch, extract_latest_commit
from clients.telegram_client import notify
from database.db import commit_status, add_details
from services.message_builder import build_message
from utils.errors import APIRateLimitedError, NetworkError, APIResponseError


def run_pipeline():
    try:
        data = fetch()
        latest = extract_latest_commit(data)
        sha = latest['sha']

        if commit_status(sha):
            logging.info("No new commit detected")
        else:
            inserted = add_details(latest)

            if inserted:
                logging.info("New commit saved successfully")
                message = build_message(latest)
                notify(message)
            else:
                logging.warning("Duplicate commit skipped")

    except APIRateLimitedError as e:
        logging.error(f"Rate limit error: {e}")

    except NetworkError as e:
        logging.error(f"Network error: {e}")

    except APIResponseError as e:
        logging.error(f"API error: {e}")

    except Exception as e:
        logging.exception(f"Unexpected crash: {e}")