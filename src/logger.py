from datetime import datetime
import logging

import pytz


def setup_logger(parsed_args, logfile_name):
    # use UTC time in log messages
    logging.Formatter.converter = lambda *args: datetime.now(tz=pytz.UTC).timetuple()
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, parsed_args.log_verbosity.upper()))

    if parsed_args.log_output == "logfile":
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S UTC",
            ),
        )
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S UTC",
            ),
        )
        logger.addHandler(console_handler)
