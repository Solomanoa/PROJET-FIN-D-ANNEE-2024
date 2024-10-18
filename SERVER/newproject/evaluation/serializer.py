from rest_framework import serializers
from .models import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'etudiant', 'enseignant', 'date_evaluation', 'heure_evaluation','maitrise_sujet','clarte_explicative','interaction_apprenant','qualite_support' ,'gestion_temps','note', 'commentaire']
        read_only_fields = ['date_evaluation', 'heure_evaluation']

    def validate_note(self, value):
        """Validation pour s'assurer que la note est un entier positif."""
        if value < 0:
            raise serializers.ValidationError("La note doit être un entier positif.")
        return value
