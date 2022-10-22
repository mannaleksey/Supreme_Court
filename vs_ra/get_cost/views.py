from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    person = {'name': f'ABA'}
    for key in request.GET:
        person[key] = request.GET[key]
    return Response(person)
