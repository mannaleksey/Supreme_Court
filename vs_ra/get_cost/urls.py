from django.urls import path
from . import views

urlpatterns = [
    path('get_cost', views.getData),
]
