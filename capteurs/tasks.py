import os
import pickle
import numpy as np
import pandas as pd
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests  # Pour l'envoi de notifications Telegram
from .models import DonneesCapteur

# Unifiez ici le nom du fichier de votre modèle de prédiction
# Par exemple, weather_model.pkl (au lieu de climate_model.pkl)
WEATHER_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'weather_model.pkl')
ANOMALY_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'anomaly_model.pkl')

@shared_task
def retrain_model():
    """
    Récupère toutes les données, réentraîne le modèle de prédiction
    et sauvegarde le modèle mis à jour.
    """
    qs = DonneesCapteur.objects.all()
    if not qs.exists():
        return "Aucune donnée disponible pour réentraînement."

    # Prépare les données
    data = pd.DataFrame(list(qs.values('humidite', 'pression', 'qualite_air', 'temperature')))
    X = data[['humidite', 'pression', 'qualite_air']]
    y = data['temperature']

    # Entraînement d'un modèle de régression, par ex. RandomForest
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Sauvegarde du modèle
    with open(WEATHER_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    return "Modèle (weather_model.pkl) réentraîné avec succès."

@shared_task
def check_anomalies_and_send_alerts():
    """
    Vérifie les dernières mesures (par ex. les 10 dernières) pour détecter des anomalies
    à l'aide du modèle d'anomalie. Envoie une alerte par e-mail et Telegram si anomalie.
    """
    # Récupération des 10 dernières mesures
    qs = DonneesCapteur.objects.order_by('-date_heure')[:10]
    if not qs.exists():
        return "Aucune donnée disponible pour la détection d'anomalie."

    # Chargement ou entraînement initial du modèle d'anomalie
    if os.path.exists(ANOMALY_MODEL_PATH):
        with open(ANOMALY_MODEL_PATH, 'rb') as f:
            anomaly_model = pickle.load(f)
    else:
        from sklearn.ensemble import IsolationForest
        full_data = pd.DataFrame(list(DonneesCapteur.objects.values(
            'temperature', 'humidite', 'pression', 'qualite_air'
        )))
        anomaly_model = IsolationForest(contamination=0.05, random_state=42)
        anomaly_model.fit(full_data)
        with open(ANOMALY_MODEL_PATH, 'wb') as f:
            pickle.dump(anomaly_model, f)

    # Préparation des données récentes à contrôler
    recent_data = pd.DataFrame(list(qs.values('temperature','humidite','pression','qualite_air')))
    predictions = anomaly_model.predict(recent_data)
    anomalies = recent_data[predictions == -1]

    if anomalies.empty:
        return "Aucune anomalie détectée."

    # S’il y a anomalie, on prépare le message
    subject = "Alerte Anomalie - Station Climatique"
    message = (
        "Des anomalies ont été détectées dans les mesures récentes:\n\n"
        + anomalies.to_string(index=False)
    )

    # 1) Envoi de l'e-mail
    try:
        recipient_list = [settings.ALERT_EMAIL]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail d'alerte: {e}")

    # 2) Envoi d'une alerte Telegram
    try:
        # Vérifiez que vous avez bien défini TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_id, "text": message}
            requests.post(url, data=data)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'alerte Telegram: {e}")

    return "Anomalie détectée, alertes envoyées par e-mail et Telegram."
