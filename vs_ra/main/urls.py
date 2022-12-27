from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='https://vs-ra.org/'), name='home'),  # включить при загрузке на сервер
    path('search', views.search, name='search'),
    path('detail', views.detail, name='detail'),
    path('reload/v1/db/every_day', views.reload_search, name='reload'),
    path('hearing', views.hearing, name='hearing'),
    path('reload/v1/db/hearing/every_day', views.reload_hearing, name='reload'),
]
