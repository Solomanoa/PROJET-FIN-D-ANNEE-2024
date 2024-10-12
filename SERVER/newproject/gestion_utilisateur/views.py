from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from face_recognition import load_image_file, face_encodings, compare_faces
from .models import Utilisateur, Etudiant, Enseignant, Administrateur, ResponsablePedagogique
from .serializer import (
    UtilisateurSerializer,
    EtudiantSerializer,
    EnseignantSerializer,
    AdministrateurSerializer,
    ResponsablePedagogiqueSerializer,
)
import base64

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import os

# Récupérer tous les utilisateurs
@api_view(['GET'])
def get_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    serialized_data = UtilisateurSerializer(utilisateurs, many=True).data
    return Response(serialized_data)

@api_view(['POST'])
def create_utilisateur(request):
    data = request.data
    serializer = UtilisateurSerializer(data=data)
    
    if serializer.is_valid():
        utilisateur = serializer.save()  # Crée l'utilisateur

        # Créer un objet en fonction du type
        if utilisateur.type == 'etudiant':
            etudiant_data = {'utilisateur': utilisateur.id, 'carte_etudiant': data.get('carte_etudiant')}
            etudiant_serializer = EtudiantSerializer(data=etudiant_data)
            if etudiant_serializer.is_valid(raise_exception=True):  # Validation ici
                etudiant_serializer.save()

        elif utilisateur.type == 'enseignant':
            enseignant_data = {'utilisateur': utilisateur.id, 'titre': data.get('titre')}
            enseignant_serializer = EnseignantSerializer(data=enseignant_data)
            if enseignant_serializer.is_valid(raise_exception=True):  # Validation ici
                enseignant_serializer.save()

        elif utilisateur.type == 'admin':
            Administrateur.objects.create(utilisateur=utilisateur)

        elif utilisateur.type == 'responsable':
            responsable_data = {'utilisateur': utilisateur.id, 'role': data.get('role')}
            responsable_serializer = ResponsablePedagogiqueSerializer(data=responsable_data)
            if responsable_serializer.is_valid(raise_exception=True):  # Validation ici
                responsable_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Récupérer un utilisateur par ID
@api_view(['GET'])
def get_utilisateur(request, id):
    try:
        utilisateur = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_data = UtilisateurSerializer(utilisateur)
    return Response(serialized_data.data)

# Mettre à jour un utilisateur
@api_view(['PUT'])
def update_utilisateur(request, id):
    try:
        utilisateur = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UtilisateurSerializer(utilisateur, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Supprimer un utilisateur
@api_view(['DELETE'])
def delete_utilisateur(request, id):
    try:
        utilisateur = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    utilisateur.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def authenticate_face(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if not image_file:
            return JsonResponse({'message': 'Aucune image fournie'}, status=400)

        # Charge l'image capturée et récupère son encodage
        try:
            uploaded_image = load_image_file(image_file)
            uploaded_encoding = face_encodings(uploaded_image)
        except Exception as e:
            return JsonResponse({'message': 'Erreur lors du chargement de l\'image : ' + str(e)}, status=500)

        if not uploaded_encoding:
            return JsonResponse({'message': 'Aucun visage détecté dans l\'image capturée'}, status=400)

        uploaded_encoding = uploaded_encoding[0]

        # Parcours des utilisateurs pour vérifier la correspondance des visages
        for user in Utilisateur.objects.all():
            if user.photo:  # Vérifiez que l'utilisateur a bien une photo
                known_image_path = user.photo.path  # Récupère le chemin complet de l'image
                if os.path.exists(known_image_path):
                    try:
                        known_image = load_image_file(known_image_path)
                        known_encoding = face_encodings(known_image)
                    except Exception as e:
                        continue  # Passe à l'utilisateur suivant en cas d'erreur

                    if known_encoding:
                        known_encoding = known_encoding[0]
                        # Compare les visages
                        results = compare_faces([known_encoding], uploaded_encoding)

                        if results[0]:  # Si une correspondance est trouvée
                            user_info = {
                                'email': user.email,
                                'nom': user.nom,
                                'prenom': user.prenom,
                                'pseudo': user.pseudo,
                                'tel': user.tel,
                                'matricule': user.matricule,
                            }
                            return JsonResponse({'message': 'Authentification réussie', 'user_info': user_info})

        return JsonResponse({'message': 'Aucun utilisateur correspondant trouvé'}, status=404)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)