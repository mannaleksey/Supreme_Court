import os
import time

from celery import shared_task
from .models import DataCase
from .temp import main


@shared_task
def refresh_db():
    while True:
        try:
            DataCase.objects.all().delete()
            print('All removed')
            main()
            print('Nice')
            break
        except:
            time.sleep(5)
            pass
