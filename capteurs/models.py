from django.db import models

class DonneesCapteur(models.Model):
    temperature = models.FloatField()
    humidite = models.FloatField()
    pression = models.FloatField()
    qualite_air = models.FloatField()
    date_heure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Données du {self.date_heure}"