from django.urls import path
from . import views

urlpatterns = [
    path('load_cost', views.loadData),
    path('get_cost', views.getData),
]
