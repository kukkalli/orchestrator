import logging
import os


class LoggingHandler:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        if "DEBUG" in os.environ:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)


def logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    log = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log


def main():
    _logger = LoggingHandler()
    _logger.log.info("Hello Hanif!")


if __name__ == "__main__":
    main()
