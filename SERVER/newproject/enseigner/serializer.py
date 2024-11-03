from rest_framework import serializers
from .models import Enseigner

class EnseignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseigner
        fields = ['id', 'enseignant', 'niveau']
        read_only_fields = ['id']  # L'ID est généralement en lecture seule lors de la création
