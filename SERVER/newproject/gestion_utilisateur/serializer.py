from rest_framework import serializers
from .models import Utilisateur, Etudiant, Enseignant, Administrateur, ResponsablePedagogique

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'pseudo', 'tel','matricule','photo', 'empreinte_digitale', 'type', 'is_active']

class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['carte_etudiant', 'utilisateur']

        def create(self, validated_data):
            # Créer l'étudiant
            etudiant = Etudiant.objects.create(**validated_data)

            # Générer le QR code pour l'étudiant
            etudiant.generate_qr_code()

            # Sauvegarder avec le QR code généré
            etudiant.save()

            return etudiant

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = ['titre', 'utilisateur']

class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ['utilisateur']

class ResponsablePedagogiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsablePedagogique
        fields = ['role', 'utilisateur']
