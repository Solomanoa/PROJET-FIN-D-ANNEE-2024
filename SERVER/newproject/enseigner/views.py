from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
    serializer = EnseignerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
