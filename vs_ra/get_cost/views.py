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
    if ('source' in keys_list) and ('dest' in keys_list) and ('price' in keys_list):
        if 'source' in keys_list:
            source_course = get_course('BUY', request.GET['source'])
        if 'dest' in keys_list:
            dest_course = get_course('SELL', request.GET['dest'])
        print(source_course, dest_course)
        data['result'] = str(round(Decimal(request.GET['price']) / source_course * dest_course, 2))
    return Response(data)
