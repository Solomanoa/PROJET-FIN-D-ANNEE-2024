from rest_framework.decorators import api_view
from django.db.models import Q
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
import zbarlight
from PIL import Image
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import hashlib
import io
import os

# Récupérer tous les utilisateurs
@api_view(['GET'])
def get_utilisateurs(request):
   
    search_query = request.query_params.get('search', None)  # Le champ de recherche unique

    utilisateurs = Utilisateur.objects.all()

    if search_query:
        # Appliquer des filtres sur plusieurs champs
        utilisateurs = utilisateurs.filter(
            Q(nom__icontains=search_query) |    # Rechercher dans le nom
            Q(prenom__icontains=search_query) | # Rechercher dans le prénom
            Q(email__icontains=search_query) |  # Rechercher dans l'email
            Q(pseudo__icontains=search_query) | # Rechercher dans le pseudo
            Q(tel__icontains=search_query) |    # Rechercher dans le numéro de téléphone
            Q(matricule__icontains=search_query) |  # Rechercher dans le matricule
            Q(type__icontains=search_query)     # Rechercher dans le type (admin, étudiant, etc.)
        )

    serialized_data = UtilisateurSerializer(utilisateurs, many=True).data
    return Response(serialized_data)

@api_view(['POST'])
def create_utilisateur(request):
    data = request.data
    """
    empreinte_digitale = request.FILES.get('empreinte_digitale')  # Récupère le fichier binaire s'il est présent
    
    # Convertir le fichier en binaire
    if empreinte_digitale:
        empreinte_digitale_data = empreinte_digitale.read()
        data['empreinte_digitale'] = empreinte_digitale_data
    """
    serializer = UtilisateurSerializer(data=data)
    
    if serializer.is_valid():
        utilisateur = serializer.save()  # Crée l'utilisateur

       # Créer un objet en fonction du type
        if utilisateur.type == 'etudiant':
        
            etudiant_data = {
                'utilisateur': utilisateur.id
            }
            etudiant_serializer = EtudiantSerializer(data=etudiant_data)
            if etudiant_serializer.is_valid(raise_exception=True):
                etudiant_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
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


@api_view(['POST'])
def authenticate_barcode(request):
    if 'barcode_image' not in request.FILES:
        return Response({"error": "Aucune image de code-barres fournie."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Charger l'image soumise
    image = Image.open(request.FILES['barcode_image'])

    # Convertir l'image pour le décodage
    image = image.convert('L')  # Convertir l'image en niveaux de gris pour faciliter le décodage
    codes = zbarlight.scan_codes('ean13', image)  # Décoder l'image

    if not codes:
        return Response({"error": "Code-barres non reconnu."}, status=status.HTTP_400_BAD_REQUEST)
    
    barcode_value = codes[0].decode('utf-8')  # Le contenu du code-barres décodé

    # Rechercher un étudiant avec ce code-barres (on suppose que c'est son ID utilisateur)
    etudiant = get_object_or_404(Etudiant, utilisateur__id=barcode_value)
    
    # Retourner une réponse avec l'étudiant authentifié
    return Response({
        "message": "Authentification réussie",
        "etudiant": {
            "nom": etudiant.utilisateur.nom,
            "prenom": etudiant.utilisateur.prenom,
            "email": etudiant.utilisateur.email,
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def authentification_empreinte(request):
    # Récupérer l'empreinte digitale soumise
    empreinte_digitale_soumise = request.FILES.get('empreinte_digitale')

    if not empreinte_digitale_soumise:
        return Response({"error": "Aucune empreinte digitale soumise."}, status=400)

    # Lire les données binaires
    empreinte_digitale_soumise_data = empreinte_digitale_soumise.read()

    # Calculer un hash de l'empreinte digitale soumise pour comparaison (ou utiliser directement les données binaires)
    empreinte_hash_soumise = hashlib.sha256(empreinte_digitale_soumise_data).hexdigest()

    # Parcourir tous les utilisateurs et vérifier si l'empreinte soumise correspond
    for utilisateur in Utilisateur.objects.all():
        if utilisateur.empreinte_digitale:
            # Calculer un hash de l'empreinte stockée pour comparaison
            empreinte_hash_stockee = hashlib.sha256(utilisateur.empreinte_digitale).hexdigest()
            if empreinte_hash_soumise == empreinte_hash_stockee:
                # Authentification réussie - retourner les informations de l'utilisateur
                serializer = UtilisateurSerializer(utilisateur)
                return Response({
                    "message": "Authentification réussie.",
                    "utilisateur": serializer.data  # Retourne les informations utilisateur
                })

    # Si aucune correspondance n'est trouvée
    return Response({"error": "Authentification échouée."}, status=400)

@api_view(['POST'])
def authenticate_qrcode(request):
    qr_data = request.data.get('qr_data')
    
    if qr_data:
        # Extraire l'ID de l'utilisateur à partir des données du QR code
        user_id = extract_user_id(qr_data)  # Implémentez cette fonction selon vos données

        try:
            etudiant = Etudiant.objects.get(utilisateur__id=user_id)
            # Authentification réussie
            user_info = {
                'id': etudiant.utilisateur.id,
                'nom': etudiant.utilisateur.nom,
                'prenom': etudiant.utilisateur.prenom,
                # Ajoutez d'autres champs si nécessaire
            }
            return Response(user_info, status=status.HTTP_200_OK)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Données QR invalides.'}, status=status.HTTP_400_BAD_REQUEST)

def extract_user_id(qr_data):
    # Cette fonction doit extraire l'ID de l'utilisateur du QR code
    # Par exemple, si votre QR code est sous la forme "ID:1 | Nom:John", 
    # alors vous pouvez faire le parsing ici.
    parts = qr_data.split('|')
    for part in parts:
        if part.startswith('ID:'):
            return int(part.split(':')[1].strip())
    return None