import logging

QTLIZ_LIB_LOGGER_NAME = "QtLiz"
logger = logging.getLogger(QTLIZ_LIB_LOGGER_NAME)
logger.addHandler(logging.NullHandler())


def log_tests():
    """
    Funzione di test per il logger
    :return:
    """
    logger.debug("Logger di test")
    logger.info("Logger di test")
    logger.warning("Logger di test")
    logger.error("Logger di test")
    logger.critical("Logger di test")