from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    person = {'name': f'ABA'}
    try:
        person['result'] = str(int(request.GET['cost']) * 2)
    except:
        person['result'] = 'hmmm'
    return Response(person)
