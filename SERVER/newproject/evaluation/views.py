from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evaluation
from .serializer import EvaluationSerializer

# Récupérer toutes les évaluations
@api_view(['GET'])
def get_evaluations(request):
    evaluations = Evaluation.objects.all()
    serialized_data = EvaluationSerializer(evaluations, many=True).data
    return Response(serialized_data)

# Récupérer une évaluation par ID
@api_view(['GET'])
def get_evaluation(request, id):
    try:
        evaluation = Evaluation.objects.get(id=id)
        serialized_data = EvaluationSerializer(evaluation).data
        return Response(serialized_data)
    except Evaluation.DoesNotExist:
        return Response({'message': 'Évaluation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

# Créer une nouvelle évaluation
@api_view(['POST'])
def create_evaluation(request):
    data = request.data
    serializer = EvaluationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Mettre à jour une évaluation par ID
@api_view(['PUT'])
def update_evaluation(request, id):
    try:
        evaluation = Evaluation.objects.get(id=id)
    except Evaluation.DoesNotExist:
        return Response({'message': 'Évaluation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = EvaluationSerializer(evaluation, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Supprimer une évaluation par ID
@api_view(['DELETE'])
def delete_evaluation(request, id):
    try:
        evaluation = Evaluation.objects.get(id=id)
        evaluation.delete()
        return Response({'message': 'Évaluation supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
    except Evaluation.DoesNotExist:
        return Response({'message': 'Évaluation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
