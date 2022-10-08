import logging
import logging.config

"""
Set up logging. There are two logs:
    The stream printed directly to console
    The detailed info printed to a rotating log file in .\logging.conf
"""
try:
    logging.config.fileConfig('.\\common\\logging.conf', disable_existing_loggers=False)
except Exception as err:
    try:
        logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    except Exception as err:
        raise Exception(err)
logSS = logging.getLogger("ss")