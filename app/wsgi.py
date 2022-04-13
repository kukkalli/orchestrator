import logging
import time

from app import app

LOG = logging.getLogger(__name__)


if __name__ == '__main__':
    LOG.info(f"The Orchestrator Application has started at {time.time()}")
    app.run()

