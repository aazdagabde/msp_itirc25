from pathlib import Path
import os

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète (gardez-la secrète en production)
SECRET_KEY = 'votre_clé_secrète_ici'

# Mode de débogage (désactiver en production)
DEBUG = True

# Liste des hôtes autorisés
ALLOWED_HOSTS = ['*']

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'capteurs',  # Votre application
    'rest_framework',  # Django REST Framework
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration des URLs
ROOT_URLCONF = 'station_climatique.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'station_climatique.wsgi.application'

# Base de données (SQLite par défaut)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
########################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aazdagbousslama@gmail.com'
EMAIL_HOST_PASSWORD = 'rznj cmub mwye fodd'
DEFAULT_FROM_EMAIL = 'aazdagbousslama@gmail.com'
ALERT_EMAIL = 'aazdagbousslama@gmail.com'
#######################
CELERY_BEAT_SCHEDULE = {
    'retrain-model-every-hour': {
        'task': 'capteurs.tasks.retrain_model',
        'schedule': 3600.0,  # toutes les 3600 secondes (1 heure)
    },
    'check-anomalies-every-30-minutes': {
        'task': 'capteurs.tasks.check_anomalies_and_send_alerts',
        'schedule': 1800.0,  # toutes les 1800 secondes (30 minutes)
    },
}
ALERT_EMAIL = "aazdagbousslama@gmail.com"
DEFAULT_FROM_EMAIL = "aazdagbousslama@gmail.com"
TELEGRAM_BOT_TOKEN = "7852205995:AAHeF8A_WPbY4rfSYmfgZc3OSc_OSTbOues"
TELEGRAM_CHAT_ID = "5622689672"  # ID du groupe ou de la personne
