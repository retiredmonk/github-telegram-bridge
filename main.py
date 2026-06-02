from apis.github_fetch import *
from services import config_service as config
from apis.telegram_notifier import notify
from services.config_service import *
from database.storage import init_db, commit_status, add_details


def setup_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def extract_latest_commit(data: list) -> dict:
    if not data:
        raise APIResponseError("Empty commit list from GitHub API")

    return data[0]


def main():
    setup_logging()
    poll_interval = float(os.getenv('POLL_INTERVAL'))
    user = os.getenv('GITHUB_OWNER')
    repo = os.getenv('REPO_NAME')
    conn, _ = init_db()

    while True:
        try:
            data = fetch(config)
            latest = extract_latest_commit(data)

            sha = latest['sha']

            if commit_status(conn, sha):
                logging.info(f"Commit is up to date")
            else:
                logging.info(f"New commit detected! Saving")
                add_details(conn, latest)
                message = (
                    f"Latest commit in {user}/{repo}:\n\n"
                    f"{latest['commit']['message']}\n\n"
                    f"{latest['commit']['author']['name']}\\n"
                    f"{latest['sha']}\n\n"
                    f"{latest['html_url']}"
                           )

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

        logging.info(f"Sleeping for {poll_interval} seconds...\n")
        time.sleep(poll_interval)


if __name__ == "__main__":
    main()



