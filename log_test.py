import logging.config
import os
import yaml

print(f"Current working directory: {os.getcwd()}")


# Path to your logging directory and YAML file
yaml_path = 'config/logging.yaml'


with open(yaml_path, 'r', encoding="utf-8",) as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

a = 23
logger = logging.getLogger('common')
logger.debug("Logging works!")
logger.info("Info test!")
logger.warning("Warning test!")

logger.critical("The value of my variable is: %s", a)


try:
    result = 10 / 0
except ZeroDivisionError as e:
    # Log the error with stack trace using logger.error
    logger.error("Error occurred: %s", e, exc_info=True)

