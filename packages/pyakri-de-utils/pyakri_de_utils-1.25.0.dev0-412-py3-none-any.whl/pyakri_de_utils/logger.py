import logging.config
import os

import yaml


def get_logger(module: str):
    logger = logging.getLogger(module)

    # Configure logger only if not already configured
    if not logger.hasHandlers():
        logger_config_file = os.getenv("LOG_CONFIG_FILE")
        # if module not in logging.Logger.manager.loggerDict:
        try:
            # If log config file is set in the env, use the handlers from there,
            # Else, redirect to stdout
            with open(logger_config_file, "r") as file:
                config = yaml.safe_load(file.read())
                logging.config.dictConfig(config)
        except Exception:
            if logger_config_file:
                logging.warning(
                    f"Failed to create logger using the config file {logger_config_file}"
                )
            stream_handler = logging.StreamHandler()
            logger.addHandler(stream_handler)

            logger.info("No config found for logger. Redirecting to Standard output!")

    return logger
