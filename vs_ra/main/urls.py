from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('detail', views.detail, name='detail'),
    path('reload/v1/db/every_day', views.reload, name='reload'),
]
