from decimal import Decimal

import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view



headers = {
    'clienttype': 'android',
    'lang': 'vi',
    'versioncode': '14004',
    'versionname': '1.40.4',
    'BNC-App-Mode': 'pro',
    'BNC-Time-Zone': 'Asia/Ho_Chi_Minh',
    'BNC-App-Channel': 'play',
    'BNC-UUID': '067042cf79631252f1409a9baf052e1a',
    'referer': 'https://www.binance.com/',
    'Cache-Control': 'no-cache, no-store',
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': 'UeokiKzPh0evwMSo5p3P6GaCyttA7jFEVMNodmDYLQlMCHpJ7sd24NkPq529yUZk',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'okhttp/4.9.0'
}


def get_cost(cost):
    asset = 'USDT'
    trade_type = 'BUY'
    payment = 'TinkoffNew'
    response = requests.post(
        url='https://www.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
        headers=headers,
        json={
            'asset': asset,
            'tradeType': f'{trade_type}',
            'fiat': 'RUB',
            'transAmount': cost,
            'page': '1',
            'payTypes': [payment],
            'rows': '1',
        }
    )
    response_json = response.json()
    price = Decimal(response_json['data'][0]['adv']['price'].replace(',', ''))
    price_usdt = Decimal(cost)/price

    asset = 'USDT'
    trade_type = 'SELL'
    payment = 'KaspiBank'
    response = requests.post(
        url='https://www.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
        headers=headers,
        json={
            'asset': asset,
            'tradeType': f'{trade_type}',
            'fiat': 'KZT',
            'page': '1',
            'payTypes': [payment],
            'rows': '10',
        }
    )
    response_json = response.json()
    for order in response_json['data']:
        max_price_usdt = Decimal(order['adv']['dynamicMaxSingleTransQuantity'])
        min_price_usdt = Decimal(order['adv']['minSingleTransQuantity'])
        if min_price_usdt <= price_usdt <= max_price_usdt:
            return str(round(Decimal(order['adv']['price']) * price_usdt, 2))
    return 'Что-то пошло не так'


@api_view(['GET'])
def getData(request):
    data = {}
    try:
        data['result'] = str(get_cost(request.GET['cost']))
    except:
        data['result'] = 'hmmm'
    return Response(data)
