import requests


def get(url, params=None, headers=None, timeout=30):
    """
    http request by Get method
    :param url:
    :param params: default None
    :param headers: default None
    :param timeout: default 30s
    :return: e.g. {'code': 200, 'content': '', 'reason': 'ok'}
    """
    res = requests.get(url, params=params, headers=headers, timeout=timeout)
    return {'code': res.status_code, 'reason': res.reason, 'content': res.content}


def get_json(url, params=None, headers=None, timeout=30):
    """
    http request by Get method,return content is json
    :param url:
    :param params: default None
    :param headers: default None
    :param timeout: default 30s
    :return: e.g. {'code': 200, 'content': json, 'reason': 'ok'}
    """
    res = requests.get(url, params=params, headers=headers, timeout=timeout)
    return {'code': res.status_code, 'reason': res.reason, 'content': res.json()}


def post(url, params=None, headers=None, timeout=30):
    """
    http request by Post method
    :param timeout: default 30s
    :param url:
    :param params: default None
    :param headers: default None
    :return:
    """
    res = requests.post(url, data=params, headers=headers, timeout=timeout)
    return {'code': res.status_code, 'reason': res.reason, 'content': res.content}


def post_json(url, params=None, headers=None, timeout=30):
    """
    http request by Post method with json(request body, response content is json)
    :param url:
    :param params: default None
    :param headers: default None
    :param timeout: default 30s
    :return: e.g. {'code': 200, 'content': json, 'reason': 'ok'}
    """
    res = requests.post(url, json=params, headers=headers, timeout=timeout)
    return {'code': res.status_code, 'reason': res.reason, 'content': res.json()}
