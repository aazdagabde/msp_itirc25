from django.urls import path
from .views import (
    home,
    afficher_donnees,
    charts_temperature,
    charts_humidite,
    charts_pression,
    charts_airquality,
    dernieres_valeurs,
    predict_weather,
    DonneesCapteurListCreate,
    api_reception_donnees,
)

urlpatterns = [
    path('', home, name='home'),
    path('donnees/', afficher_donnees, name='afficher_donnees'),
    path('charts/temperature/', charts_temperature, name='charts_temperature'),
    path('charts/humidite/', charts_humidite, name='charts_humidite'),
    path('charts/pression/', charts_pression, name='charts_pression'),
    path('charts/airquality/', charts_airquality, name='charts_airquality'),
    path('dernieres_valeurs/', dernieres_valeurs, name='dernieres_valeurs'),
    path('predictions/', predict_weather, name='predict_climate'),
    path('api/donnees/', DonneesCapteurListCreate.as_view(), name='donnees-capteur-list'),
    path('api/reception-esp/', api_reception_donnees, name='api_reception_esp'),
]
