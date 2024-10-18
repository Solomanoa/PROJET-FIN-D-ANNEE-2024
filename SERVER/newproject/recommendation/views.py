from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recommendation
from .serializers import RecommendationSerializer

@api_view(['GET'])
def get_recommendations(request):
    recommendations = Recommendation.objects.all()
    serialized_data = RecommendationSerializer(recommendations, many=True).data
    return Response(serialized_data)

@api_view(['GET'])
def get_recommendation(request, id):
    try:
        recommendation = Recommendation.objects.get(id=id)
        serialized_data = RecommendationSerializer(recommendation).data
        return Response(serialized_data)
    except Recommendation.DoesNotExist:
        return Response({'message': 'Recommandation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_recommendation(request):
    data = request.data
    serializer = RecommendationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_recommendation(request, id):
    try:
        recommendation = Recommendation.objects.get(id=id)
    except Recommendation.DoesNotExist:
        return Response({'message': 'Recommandation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = RecommendationSerializer(recommendation, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_recommendation(request, id):
    try:
        recommendation = Recommendation.objects.get(id=id)
        recommendation.delete()
        return Response({'message': 'Recommandation supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
    except Recommendation.DoesNotExist:
        return Response({'message': 'Recommandation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
