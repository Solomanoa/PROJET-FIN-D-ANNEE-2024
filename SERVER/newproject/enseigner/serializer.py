from rest_framework import serializers
from .models import Enseigner

class EnseignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseigner
        fields = ['id', 'enseignant', 'etudiants']
        read_only_fields = ['id']  # L'ID est généralement en lecture seule lors de la création

    def validate_etudiants(self, value):
        """Validation pour s'assurer qu'au moins un étudiant est sélectionné."""
        if not value:
            raise serializers.ValidationError("Au moins un étudiant doit être associé à l'enseignant.")
        return value
