import json
import datetime
import os
import pickle
import numpy as np
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import StandardScaler
from .models import DonneesCapteur
from .serializers import DonneesCapteurSerializer

# Chemins vers les modèles ML
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEATHER_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'weather_model.pkl')
ANOMALY_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'anomaly_model.pkl')

# Chargement des modèles
with open(WEATHER_MODEL_PATH, 'rb') as f:
    weather_model = pickle.load(f)

with open(ANOMALY_MODEL_PATH, 'rb') as f:
    anomaly_data = pickle.load(f)
    anomaly_model = anomaly_data['model']
    scaler = anomaly_data['scaler']

# Page d'accueil
def home(request):
    return render(request, 'capteurs/home.html')

# API REST pour ESP8266
@api_view(['POST'])
def api_reception_donnees(request):
    serializer = DonneesCapteurSerializer(data=request.data)
    if serializer.is_valid():
        donnees = serializer.save()

        X = np.array([[donnees.temperature, donnees.humidite, donnees.pression, donnees.qualite_air]])
        X_scaled = scaler.transform(X)

        pluie = bool(weather_model.predict(X)[0])
        anomalie = anomaly_model.predict(X_scaled)[0] == -1

        return Response({"pluie": pluie, "anomalie": anomalie}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Affichage des données
def afficher_donnees(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values()), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/afficher_donnees.html', {'donnees_json': donnees_json})

def charts_temperature(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'temperature')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_temperature.html', {'donnees_json': donnees_json})

def charts_humidite(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'humidite')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_humidite.html', {'donnees_json': donnees_json})

def charts_pression(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'pression')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_pression.html', {'donnees_json': donnees_json})

def charts_airquality(request):
    qs = DonneesCapteur.objects.all().order_by('-date_heure')
    donnees_json = json.dumps(list(qs.values('date_heure', 'qualite_air')), cls=DjangoJSONEncoder)
    return render(request, 'capteurs/charts_airquality.html', {'donnees_json': donnees_json})

def dernieres_valeurs(request):
    try:
        derniere_donnee = DonneesCapteur.objects.latest('date_heure')
    except DonneesCapteur.DoesNotExist:
        derniere_donnee = None
    time_passed = timezone.now() - derniere_donnee.date_heure if derniere_donnee else None
    return render(request, 'capteurs/dernieres_valeurs.html', {
        'derniere_donnee': derniere_donnee,
        'time_passed': time_passed,
    })

# Prédictions météo et anomalies
def predict_weather(request):
    try:
        qs = DonneesCapteur.objects.all().order_by('-date_heure')[:100]
        if not qs:
            raise ValueError("Aucune donnée disponible")

        X = np.array([[d.temperature, d.humidite, d.pression, d.qualite_air] for d in reversed(qs)])
        X_scaled = scaler.transform(X)

        predictions_pluie = weather_model.predict(X)
        anomalies = anomaly_model.predict(X_scaled)

        results = [{
            'date_heure': d.date_heure,
            'temperature': d.temperature,
            'humidite': d.humidite,
            'pression': d.pression,
            'qualite_air': d.qualite_air,
            'pluie_predite': "Pluie" if pluie == 1 else "Pas de pluie",
            'anomalie': anomalie == -1
        } for d, pluie, anomalie in zip(reversed(qs), predictions_pluie, anomalies)]

        context = {'results': results, 'generated_at': timezone.now()}
        return render(request, 'capteurs/predictions.html', context)

    except Exception as e:
        return render(request, 'capteurs/predictions.html', {'error': str(e)})

class DonneesCapteurListCreate(generics.ListCreateAPIView):
    queryset = DonneesCapteur.objects.all()
    serializer_class = DonneesCapteurSerializer