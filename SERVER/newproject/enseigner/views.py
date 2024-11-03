from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from gestion_utilisateur.models import Enseignant
from .models import Enseigner
from .serializer import EnseignerSerializer

# Récupérer toutes les associations Enseigner
@api_view(['GET'])
def get_enseignements(request):
    enseignements = Enseigner.objects.all()
    serialized_data = EnseignerSerializer(enseignements, many=True).data
    return Response(serialized_data)

# Récupérer une association Enseigner par ID
@api_view(['GET'])
def get_enseignement(request, id):
    enseignement = get_object_or_404(Enseigner, id=id)
    serialized_data = EnseignerSerializer(enseignement).data
    return Response(serialized_data)

# Créer une nouvelle association Enseigner
@api_view(['POST'])
def create_enseignement(request):
    data = request.data

    # Vérifiez que l'ID de l'enseignant est fourni dans la requête
    if 'enseignant' not in data:
        return Response({"enseignant": ["ID de l'enseignant manquant."]}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifiez l'existence de l'enseignant
    try:
        enseignant = Enseignant.objects.get(utilisateur__id=data['enseignant'])
    except Enseignant.DoesNotExist:
        return Response({"enseignant": ["Enseignant non trouvé."]}, status=status.HTTP_404_NOT_FOUND)

    # Utilisez l'ID de l'utilisateur pour créer l'objet Enseigner
    serializer = EnseignerSerializer(data={'enseignant': enseignant.utilisateur.id, 'niveau': data.get('niveau')})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Imprimez les erreurs pour le débogage
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Mettre à jour une association Enseigner par ID
@api_view(['PUT'])
def update_enseignement(request, id):
    enseignement = get_object_or_404(Enseigner, id=id)
    data = request.data
    serializer = EnseignerSerializer(enseignement, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Supprimer une association Enseigner par ID
@api_view(['DELETE'])
def delete_enseignement(request, id):
    enseignement = get_object_or_404(Enseigner, id=id)
    enseignement.delete()
    return Response({'message': 'Association Enseigner supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)


