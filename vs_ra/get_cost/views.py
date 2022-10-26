import json
import time
from decimal import Decimal
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models_peewee import get_course


@api_view(['GET'])
def getData(request):
    data = {}
    keys_list = list(request.GET.keys())
    dict_temp = {}
    for key, value in request.GET.items():
        dict_temp[key] = value
    with open('temp.json', 'w', encoding='utf-8') as file:
        json.dump(dict_temp, file)
    if ('source' in keys_list) and ('dest' in keys_list) and ('price' in keys_list):
        try:
            if 'source' in keys_list:
                source_course = get_course('BUY', request.GET['source'])
            if 'dest' in keys_list:
                dest_course = get_course('SELL', request.GET['dest'])
            if source_course and dest_course:
                data['result'] = str(round(Decimal(request.GET['price']) / source_course * dest_course, 2))
        except:
            data['result'] = '0'
    else:
        data['result'] = '0'
    return Response(data)
