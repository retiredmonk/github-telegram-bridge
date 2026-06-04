import logging
import time
from env import get_settings
from services.monitor_pipeline import run_pipeline
from utils.logger import setup_logging


def main():
    setup_logging()
    settings = get_settings()
    while True:
        run_pipeline()
        logging.info(f"Sleeping for {settings.POLL_INTERVAL} seconds...\n")
        time.sleep(settings.POLL_INTERVAL)

if __name__ == "__main__":
    main()

