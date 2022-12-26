import os
import time

from celery import shared_task
from .models import DataCase, TextsCase, HearingCase
from .update_db_search import update_db_search
from .update_db_hearing import update_db_hearing


@shared_task
def refresh_db():
    print('start')
    while True:
        try:
            DataCase.objects.all().delete()
            TextsCase.objects.all().delete()
            break
        except:
            time.sleep(5)
            pass
    print('All removed')
    update_db_search()
    print('Nice')


@shared_task
def refresh_db_hearing():
    print('start')
    while True:
        try:
            HearingCase.objects.all().delete()
            break
        except:
            time.sleep(5)
            pass
    print('All removed')
    update_db_hearing()
    print('Nice')
