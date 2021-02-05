from django.urls import path
from . import views

app_name = "gemsdeals"

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('loadcsv', views.loadcsv, name='loadcsv'),
    path('result', views.result, name='result'),
    path('simpleoutput', views.simpleoutput, name='simpleoutput'),
    path('jsonoutput', views.jsonoutput, name='jsonoutput'),
    path('cleardatabase', views.cleardatabase, name='cleardatabase'),
]
