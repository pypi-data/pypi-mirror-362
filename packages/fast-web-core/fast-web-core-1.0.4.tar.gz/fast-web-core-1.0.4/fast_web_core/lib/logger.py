import logging


def get(name: str = '', tag: str = '') -> logging.Logger:
    """
    get logger of specific tag
    :param name: name of the logger
    :param tag: tag of the logger
    :return: logger instance
    """
    if tag:
        logger_name = (tag + '_' + name).upper()
    else:
        logger_name = name.upper()
    return logging.getLogger(logger_name)


def for_handler(name: str) -> logging.Logger:
    """
    get handler logger
    :param name: handler name
    :return: controller logger
    """
    return get('handler', name)


def for_middleware(name: str) -> logging.Logger:
    """
    get middleware logger
    :param name: middleware name
    :return: middleware logger
    """
    return get('middleware', name)


def for_model(name: str) -> logging.Logger:
    """
    get model logger
    :param name: model name
    :return: model logger
    """
    return get('model', name)


def for_service(name: str) -> logging.Logger:
    """
    get service logger
    :param name: service name
    :return: service logger
    """
    return get('service', name)


def for_job(name: str) -> logging.Logger:
    """
    get job logger
    :param name: job name
    :return: job logger
    """
    return get('job', name)


def for_provider(name: str) -> logging.Logger:
    """
    get provider logger
    :param name: provider name
    :return: provider logger
    """
    return get('provider', name)


def for_util(name: str) -> logging.Logger:
    """
    get util logger
    :param name: util name
    :return: util logger
    """
    return get('util', name)


def for_client(name: str) -> logging.Logger:
    """
    get client logger
    :param name: client name
    :return: client logger
    """
    return get('client', name)
