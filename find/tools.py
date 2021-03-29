import math
from collections import Counter

import requests


def find_duplicates(array: list) -> list:
    """Находии дупликаты"""
    count = Counter(array)
    result = [element for element in count.keys() if count[element] > 1]
    return result


def make_batch(size, state):
    """Формируем batch-запрос"""
    request = '&halt=0'
    for i in range(state, state + size):
        request += f'&cmd[cmd{i}]=crm.company.list?start={50*i}'
    return request


def get_all_companies_titles(access_token, domain):
    """Получаем все названия кампаний"""
    url = 'https://' + domain + '/rest/crm.company.list?access_token=' + access_token
    r = requests.get(url)
    total = r.json()['total']
    batch_req = math.ceil(total / 2500)
    batch_url = 'https://' + domain + '/rest/batch?auth=' + access_token
    titles = []
    for batch_num in range(batch_req - 1):
        state = batch_num * 50
        params = make_batch(50, state)
        r = requests.get(batch_url + params)
        result = r.json()['result']['result']
        for cmd in result:
            titles += [company['TITLE'] for company in result[cmd]]
    size = math.ceil((total % 2500) / 50)
    params = make_batch(size, (batch_req - 1) * 50)
    r = requests.get(batch_url + params)
    result = r.json()['result']['result']
    for cmd in result:
        titles += [company['TITLE'] for company in result[cmd]]
    return titles
