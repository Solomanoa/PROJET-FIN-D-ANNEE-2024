from rest_framework import serializers
from .models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'responsable', 'enseignant', 'recommandation', 'date_recommendation']
        read_only_fields = ['date_recommendation']  # La date est automatiquement définie lors de la création
