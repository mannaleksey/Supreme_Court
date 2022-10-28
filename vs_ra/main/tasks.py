import os
import time

from celery import shared_task
from .models import DataCase, TextsCase
from .temp import main


@shared_task
def refresh_db():
    # try:
        DataCase.objects.all().delete()
        TextsCase.objects.all().delete()
        print('All removed')
        main()
        print('Nice')
    # except:
    #     time.sleep(5)
    #     pass
