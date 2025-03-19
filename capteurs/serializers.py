from rest_framework import serializers
from .models import DonneesCapteur

class DonneesCapteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonneesCapteur
        fields = '__all__'